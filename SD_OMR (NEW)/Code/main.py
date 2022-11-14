# <editor-fold desc="FILE DESCRIPTION">
# DESCRIPTION :
#       This file serves as the entry point of the program where the execution begins
#
#  PUBLIC FUNCTIONS :
#       None
#
#  NOTES :
#       None
#
#  AUTHOR :    B1499 JEREMY PUN
#
#  CHANGES :
#       None
#
# </editor-fold>

# <editor-fold desc="LIBRARY">
# 1. cv2       : Import cv2 library, computer vision AI
# 2. numpy     : Import numpy library, enable AI to identify pixels as O and 1
# 3. utility   : Import utility file, all user-defined functions are retrieved from here
# </editor-fold>
import cv2
import numpy as np
import utility

# <editor-fold desc="IMAGE FORMAT">
# 1. Guide     :
    # • Adjust widthImg, height to improve clarity
# </editor-fold>
# path= "../Resources/OMR_Long_Short.png"
path= "../Resources/OMR_Blank.png"
widthImg=400
heightImg=1000

# <editor-fold desc="OMR QUESTION FORMAT">
# 1. question  , The number of questions to detect
# 2. choices   , The number of choices per question
# 3. ans       , The answer sheet
# </editor-fold>
questions=20
choices=4
# ans = [0,1,2,3,2,1,0,1,2,3,2,1,0,1,2,3,2,1,0,2]
ans = [0,1,2,3,2,1,0,1,2,3,2,1,0,1,2,3,2,1,0,0]         #Test case: More than 1 answer

#ENABLE WEBCAM CAPTURE (21-09-2022)#
# webcamFeed = True
# cameraNo = 0 # 0 means the default camera
# capture =cv2.VideoCapture(cameraNo)
# capture.set(10,150)

# while True:
    # if webcamFeed: success, img=capture.read()
    # else: img=cv2.imread(path)
#ENABLE WEBCAM CAPTURE (21-09-2022)#

# PREPROCESSING
img=cv2.imread(path)                                   # Retrieve image
img=cv2.resize(img,(widthImg,heightImg))
imgContours=img.copy()
imgFinal=img.copy()
imgBiggestContours=img.copy()
imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)           # Convert image to gray image
imgBlur=cv2.GaussianBlur(imgGray,(5,5),1)              # Blur the image
imgCanny=cv2.Canny(imgBlur,10,50)                      # Convert blur image to canny image
try:
    # 1. FIND ALL CONTOURS
    contours, hierarchy = cv2.findContours(imgCanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    # 2. DISPLAY CONTOURS, -1 means all index,RGB Green Colour(0,255,0),thickness=10
    cv2.drawContours(imgContours,contours,-1,(0,255,0),10)

    # 3. FIND RECTANGLES
    rectCon= utility.rectContour(contours)

    # 4. FIND BIGGEST CONTOUR (BUBBLE)
    biggestContour= utility.getCornerPoints(rectCon[0])
    # print(biggestContour.shape)                           # Check values

    # 5. FIND 2nd BIGGEST CONTOUR (RESULT ZONE)
    gradePoints= utility.getCornerPoints(rectCon[1])

    # 6. LOCATE BUBBLE and RESULT ZONE
    if biggestContour.size!=0 and gradePoints.size!=0:
        cv2.drawContours(imgBiggestContours,biggestContour,-1,(0,255,0),20)
        cv2.drawContours(imgBiggestContours,gradePoints,-1,(255,0,0),20)
        biggestContour= utility.reorder(biggestContour)
        gradePoints= utility.reorder(gradePoints)

        # 1. BIRDS EYE VIEW: BUBBLE ZONE
        pt1=np.float32(biggestContour)
        pt2=np.float32([[0,0],[widthImg,0],[0,heightImg],[widthImg,heightImg]])
        matrix=cv2.getPerspectiveTransform(pt1,pt2)
        imgWarpColored=cv2.warpPerspective(img,matrix,(widthImg,heightImg))
        # cv2.imshow("Bubble Zone",imgWarpColored)

        # 2. BIRDS EYE VIEW: GRADE ZONE
        ptGrade1=np.float32(gradePoints)
        ptGrade2=np.float32([[0,0],[325,0],[0,150],[325,150]])
        matrixGrade=cv2.getPerspectiveTransform(ptGrade1,ptGrade2)
        imgGradeDisplay=cv2.warpPerspective(img,matrixGrade,(325,150))
        # cv2.imshow("Grade",imgGradeDisplay)

        #3. APPLY THRESHOLD
        imgWarpGray = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)
        # 170 determines the intensity of the shaded region
        imgThresh =cv2.threshold(imgWarpGray,170,255,cv2.THRESH_BINARY_INV)[1]

        # 4. FIND INDIVIDUAL BUBBLES
        boxes = utility.splitBoxes(imgThresh)
        # cv2.imshow("Test",boxes[2])

        # 5. FIND MARK BUBBLES (USE Non-Zero Pixels)
        # print(cv2.countNonZero(boxes[1]),cv2.countNonZero(boxes[2]))

        # 6. GETTING NON-Zero PIXEL VALUES OF EACH BUBBLE
        myPixelValue=np.zeros((questions,choices))
        countCol=0
        countRow=0

        # Loop through all bubbles
        for image in boxes:
            totalPixels=cv2.countNonZero(image)
            # 5x5 array (5 questions and 5 choices)
            myPixelValue[countRow][countCol]=totalPixels
            countCol+=1
            if(countCol==choices):countRow+=1;countCol=0
        # print(myPixelValue)

        # FINDING INDEX VALUES OF THE MARKING
        # LOGIC: USE THE MAXIMUM VALUE, TO GET THE SHADED BUBBLE
        myIndex = []
        filter_arr = []
        questionNum = 0                             #numberLabelling
        for x in range (0,questions):
            arr= myPixelValue[x]
            print("Q",x,":",arr)                  #View question index
            myIndexVal=np.where(arr==np.amax(arr))
            # print(x,"Shaded:",myIndexVal[0])            #test for shaded bubbles
            myIndex.append(myIndexVal[0][0])
        # print(myIndex)

        #####Suggestion: Continue from here####
        # Driver code: To filter more than shaded region
        # for element in arr:
        #     # if the element is higher than 2000, set the value to True, otherwise False:
        #     if element > 2000:
        #         filter_arr.append(True)
        #     else:
        #         filter_arr.append(False)
        #
        # newarr = arr[filter_arr]
        # print(newarr)  # View values
        #
        # for x in range(0, questions):
        #     if (len(newarr) > 1):
        #         myIndexVal = None
        #     else:
        #         myIndexVal = np.where(arr == np.amax(arr))
        #         print(x,"Shaded:",myIndexVal[0])            #test for shaded bubbles
        #     myIndex.append(myIndexVal[0][0])
        #####Suggestion: Continue from here####

        # GRADING
        grading=[]
        for x in range (0,questions):
            if ans[x]==myIndex[x]:
                # 1 if answer is correct, 0 if answer is wrong
                grading.append(1)
            else: grading.append(0)
        # print(grading)
        score = sum(grading)/questions *100 # FINAL GRADE
        print(score)

        #DISPLAY ANSWERS
        imgResults = imgWarpColored.copy()
        imgResults = utility.showAnswers(imgResults, myIndex, grading, ans, questions, choices)

        #DISPLAY ANSWERS (Just shades only)
        imgRawDrawing = np.zeros_like(imgWarpColored)
        imgRawDrawing = utility.showAnswers(imgRawDrawing, myIndex, grading, ans, questions, choices)

        #DISPLAY ANSWERS (Based on original image)
        invMatrix = cv2.getPerspectiveTransform(pt2,pt1)
        imgInvWarp = cv2.warpPerspective(imgRawDrawing,invMatrix,(widthImg,heightImg))

        #DISPLAY GRADES (Based on original image)
        imgRawGrade = np.zeros_like(imgGradeDisplay)
        cv2.putText(imgRawGrade,str(int(score))+"%",(50,100),cv2.FONT_HERSHEY_COMPLEX,3,(0,255,255),3)
        # cv2.imshow("Grade",imgRawGrade)

        #DISPLAY FINAL RESULTS (Based on original image)
        invMatrixG = cv2.getPerspectiveTransform(ptGrade2,ptGrade1)
        imgInvGradeDisplay = cv2.warpPerspective(imgRawGrade, invMatrixG, (widthImg,heightImg))
        imgFinal = cv2.addWeighted(imgFinal,0.8,imgInvWarp,1,0)
        imgFinal = cv2.addWeighted(imgFinal,1,imgInvGradeDisplay,1,0)

     # print(len(biggestContour))                           # Check values
     # print(biggestContour)                                # Check values
    # 7. DISPLAY IMAGE STACK (CHECK VALUES)
    # <editor-fold desc="Description">
    # 1. Variables     :
        # • imgBlank  , A blank image
        # • imgArray  , An array to store all images
        # • labels    , Assign lables for all images
    # </editor-fold>
    imgBlank=np.zeros_like(img)
    imageArray = ([img,imgGray,imgBlur,imgCanny],
                  [imgContours,imgBiggestContours,imgWarpColored,imgThresh],
                  [imgResults,imgRawDrawing,imgInvWarp,imgFinal])
except:
    imgBlank = np.zeros_like(img)

    imageArray = ([img, imgGray, imgBlur, imgCanny],
                  [imgBlank, imgBlank, imgBlank, imgBlank],
                  [imgBlank, imgBlank, imgBlank, imgBlank]
                  )

labels = [["Original","Gray","Blur","Blur"],
          ["Contours","Biggest Contours","Warp","Threshold"],
          ["Result","Raw","Inverse","Inverse Warp","Final"]
          ]

imgStacked = utility.stackImages(imageArray, 0.4, labels)

# cv2.imshow("Original",img)                            # Display original image to test the program
cv2.namedWindow("Stacked Images", cv2.WINDOW_NORMAL)    # Enables a resizable window
cv2.imshow("Stacked Images",imgStacked)

# Keyboard input: 0xFF == ord('s') (21-09-2022)
# if cv2.waitKey(1) & 0xFF == ord('s'):
#     # SAVE IMAGE FILE
#     cv2.imwrite("FinalResult.jpg", imgFinal)
#     cv2.waitKey(300)

# # 8. DISPLAY FINAL IMAGE
cv2.imshow("Final Image", imgFinal)                     # Display finalized image
# cv2.imwrite("Test_Long_FinalResult.png", imgFinal)    # Save finalized image
cv2.waitKey(0)
# cv2.destroyAllWindows()