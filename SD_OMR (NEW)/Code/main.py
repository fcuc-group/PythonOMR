import os
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import utility
# https://roytuts.com/upload-and-display-image-using-python-flask/

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']

    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')

        path = "../Resources/One/OMR_1.png"
        # path= "../Resources/OMR_Blank.png"
        widthImg = 400
        heightImg = 1000

        # <editor-fold desc="OMR QUESTION FORMAT">
        # 1. question  , The number of questions to detect
        # 2. choices   , The number of choices per question
        # 3. ans       , The test_case sheet
        # </editor-fold>
        questions = 20
        choices = 4
        ans = [0,1,2,3,2,1,0,1,2,3,2,1,0,1,2,3,2,1,0,2]

        # PREPROCESSING
        img = cv2.imread(path)  # Retrieve image
        img = cv2.resize(img, (widthImg, heightImg))
        imgContours = img.copy()
        imgFinal = img.copy()
        imgBiggestContours = img.copy()
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert image to gray image
        imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)  # Blur the image
        imgCanny = cv2.Canny(imgBlur, 10, 50)  # Convert blur image to canny image
        # 1. FIND ALL CONTOURS
        contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # 2. DISPLAY CONTOURS, -1 means all index,RGB Green Colour(0,255,0),thickness=10
        cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10)

        # 3. FIND RECTANGLES
        rectCon = utility.rectContour(contours)

        # 4. FIND BIGGEST CONTOUR (BUBBLE)
        biggestContour = utility.getCornerPoints(rectCon[0])
        # print(biggestContour.shape)                           # Check values

        # 5. FIND 2nd BIGGEST CONTOUR (RESULT ZONE)
        gradePoints = utility.getCornerPoints(rectCon[1])

        # 6. LOCATE BUBBLE and RESULT ZONE
        if biggestContour.size != 0 and gradePoints.size != 0:
            cv2.drawContours(imgBiggestContours, biggestContour, -1, (0, 255, 0), 20)
            cv2.drawContours(imgBiggestContours, gradePoints, -1, (255, 0, 0), 20)
            biggestContour = utility.reorder(biggestContour)
            gradePoints = utility.reorder(gradePoints)

            # 1. BIRDS EYE VIEW: BUBBLE ZONE
            pt1 = np.float32(biggestContour)
            pt2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
            matrix = cv2.getPerspectiveTransform(pt1, pt2)
            imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
            # cv2.imshow("Bubble Zone",imgWarpColored)

            # 2. BIRDS EYE VIEW: GRADE ZONE
            ptGrade1 = np.float32(gradePoints)
            ptGrade2 = np.float32([[0, 0], [325, 0], [0, 150], [325, 150]])
            matrixGrade = cv2.getPerspectiveTransform(ptGrade1, ptGrade2)
            imgGradeDisplay = cv2.warpPerspective(img, matrixGrade, (325, 150))
            # cv2.imshow("Grade",imgGradeDisplay)

            # 3. APPLY THRESHOLD
            imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
            # 170 determines the intensity of the shaded region
            imgThresh = cv2.threshold(imgWarpGray, 170, 255, cv2.THRESH_BINARY_INV)[1]

            # 4. FIND INDIVIDUAL BUBBLES
            boxes = utility.splitBoxes(imgThresh)
            # cv2.imshow("Test",boxes[2])

            # 5. FIND MARK BUBBLES (USE Non-Zero Pixels)
            # print(cv2.countNonZero(boxes[1]),cv2.countNonZero(boxes[2]))

            # 6. GETTING NON-Zero PIXEL VALUES OF EACH BUBBLE
            myPixelValue = np.zeros((questions, choices))
            countCol = 0
            countRow = 0

            # Loop through all bubbles
            for image in boxes:
                totalPixels = cv2.countNonZero(image)
                # 5x5 array (5 questions and 5 choices)
                myPixelValue[countRow][countCol] = totalPixels
                countCol += 1
                if (countCol == choices): countRow += 1;countCol = 0
            # print(myPixelValue)

            # FINDING INDEX VALUES OF THE MARKING
            # LOGIC: USE THE MAXIMUM VALUE, TO GET THE SHADED BUBBLE
            myIndex = []
            filter_arr = []
            questionNum = 0  # numberLabelling
            for x in range(0, questions):
                arr = myPixelValue[x]
                print("Q", x, ":", arr)  # View question index
                myIndexVal = np.where(arr == np.amax(arr))
                # print(x,"Shaded:",myIndexVal[0])            #test for shaded bubbles
                myIndex.append(myIndexVal[0][0])
            # print(myIndex)

            # GRADING
            grading = []
            for x in range(0, questions):
                if ans[x] == myIndex[x]:
                    # 1 if test_case is correct, 0 if test_case is wrong
                    grading.append(1)
                else:
                    grading.append(0)
            # print(grading)
            score = sum(grading) / questions * 100  # FINAL GRADE
            print(score)

            # DISPLAY ANSWERS
            imgResults = imgWarpColored.copy()
            imgResults = utility.showAnswers(imgResults, myIndex, grading, ans, questions, choices)

            # DISPLAY ANSWERS (Just shades only)
            imgRawDrawing = np.zeros_like(imgWarpColored)
            imgRawDrawing = utility.showAnswers(imgRawDrawing, myIndex, grading, ans, questions, choices)

            # DISPLAY ANSWERS (Based on original image)
            invMatrix = cv2.getPerspectiveTransform(pt2, pt1)
            imgInvWarp = cv2.warpPerspective(imgRawDrawing, invMatrix, (widthImg, heightImg))

            # DISPLAY GRADES (Based on original image)
            imgRawGrade = np.zeros_like(imgGradeDisplay)
            cv2.putText(imgRawGrade, str(int(score)) + "%", (50, 100), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 255, 255),
                        3)
            # cv2.imshow("Grade",imgRawGrade)

            # DISPLAY FINAL RESULTS (Based on original image)
            invMatrixG = cv2.getPerspectiveTransform(ptGrade2, ptGrade1)
            imgInvGradeDisplay = cv2.warpPerspective(imgRawGrade, invMatrixG, (widthImg, heightImg))
            imgFinal = cv2.addWeighted(imgFinal, 0.8, imgInvWarp, 1, 0)
            imgFinal = cv2.addWeighted(imgFinal, 1, imgInvGradeDisplay, 1, 0)

        # # 8. DISPLAY FINAL IMAGE
        # cv2.imshow("Final Image", imgFinal)  # Display finalized image
        cv2.imwrite("static/uploads/Graded_OMR.png", imgFinal)  # Save finalized image
        # cv2.waitKey(0)

        return render_template('upload.html', filename="../static/uploads/Graded_OMR.png")
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__=="__main__":
    app.run(debug=True)