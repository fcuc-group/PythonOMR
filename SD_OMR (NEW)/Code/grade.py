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
import time

# <editor-fold desc="IMAGE FORMAT">
# 1. Guide     :
    # • Adjust widthImg, height to improve clarity
# </editor-fold>
# path= "../Code/static/uploads/OMR_Double_1.png"                         #Double shaded bubble
# path= "../Resources/Blank/OMR_Blank.png"                                #Blank bubbbles
# path= "../Resources/One/OMR_1.png"                                      #Blank bubbbles
# path= "../Resources/More(Single)/OMR_Single_1.png"                      #More than 1 shaded bubble
# path= "../Resources/More(Double)/OMR_Double_1.png"                      #More than 1 questions with more than 1 shaded bubbbles
# path= "../Resources/Blur.png"
# path= "../Resources/BlurAndSmall.png"
# path= "../Resources/MixBlur_Half.png"
#path= "../Resources/MixBlur_Half_2.png"
# path= "../Resources/MixSymbol.png"
# path= "../Resources/MixSymbol2.png"

def grade(path,ans):
    widthImg=400
    heightImg=1000

    # <editor-fold desc="OMR QUESTION FORMAT">
    # 1. question  , The number of questions to detect
    # 2. choices   , The number of choices per question
    # 3. ans       , The test_case sheet
    # </editor-fold>
    questions=20
    choices=4
    # ans = [0,1,2,3,2,1,0,1,2,3,2,1,0,1,2,3,2,1,0,0]         #Test case: More(Double) than 1 test_case
    #ans = [0,0,1,2,2,1,2,3,2,1,2,3,2,0,1,0,3,1,2,1]         #Test case: More(Double) than 1 test_case

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
            pixelValue=np.zeros((questions,choices))
            countCol=0
            countRow=0

            # Loop through all bubbles
            for image in boxes:
                totalPixels=cv2.countNonZero(image)
                # 5x5 array (5 questions and 5 choices)
                pixelValue[countRow][countCol]=totalPixels
                countCol+=1
                if(countCol==choices):countRow+=1;countCol=0
            # print(myPixelValue)

            # FINDING INDEX VALUES OF THE MARKING
            # LOGIC: USE THE MAXIMUM VALUE, TO GET THE SHADED BUBBLE
            shadedIndex = []
            questionNum = 0                             #numberLabelling
            for x in range (0,questions):

                # UPDATE LOGIC HERE TO REJECT MORE THAN 1 SHADED REGION
                row=pixelValue[x]
                print("Q",x+1," : ",row)
                countMore = sum(map(lambda x: (x > 2000) == 1, row))
                # countZero = sum(map(lambda x: (x < 1000) == 1, row))
                countZero = sum(map(lambda x: (x < 2000) == 1, row))
                print("countMore: ",countMore)

                #Capture more than 1 shaded bubble
                if countMore >= 2:
                    print("captured more than 1 shaded bubble")
                    row = [0, 0, 0, 0, 4]
                if countZero ==4:
                # Capture 0 shaded bubble
                    print("captured 0 shaded bubble")
                    row = [0, 0, 0, 0, 0, 5]
                #ADD CHECKING
                shadedIndexValue=np.where(row==np.amax(row))
                print("shadedIndexValue: ", shadedIndexValue)

                # UPDATE LOGIC HERE TO REJECT MORE THAN 1 SHADED REGION
                # print(x,"Shaded:",myIndexVal[0])                            #View which bubble is shaded

                shadedIndex.append(shadedIndexValue[0][0])
                # print("ShadedIndexValue: ", shadedIndexValue)

            # print(myIndex)

            # GRADING
            grading=[]

            print("Shaded Index: ", shadedIndex)

            for x in range (0,questions):

                if shadedIndex[x]==5:
                    grading.append(5)
                    print("Q",x+1," : Not shaded")
                elif shadedIndex[x]==4:
                    grading.append(4)
                    print("Q",x+1," : More than 1 shaded bubble detected")
                else:
                    if ans[x]==shadedIndex[x]:
                        # 1 if test_case is correct, 0 if test_case is wrong
                        grading.append(1)
                    else :
                        grading.append(0)

            # print(grading)
            gradingSum = sum(i for i in grading if i!= 4 and i!=5)
            score = gradingSum/questions *100 # FINAL SCORE

            # score = sum(grading)/questions *100 # FINAL SCORE
            print("Grading: ",grading)
            print("Score: ",score)

            #DISPLAY ANSWERS
            imgResults = imgWarpColored.copy()
            imgResults = utility.showAnswers(imgResults, shadedIndex, grading, ans, questions, choices)

            #DISPLAY ANSWERS (Just shades only)
            imgRawDrawing = np.zeros_like(imgWarpColored)
            imgRawDrawing = utility.showAnswers(imgRawDrawing, shadedIndex, grading, ans, questions, choices)

            #DISPLAY ANSWERS (Based on original image)
            invMatrix = cv2.getPerspectiveTransform(pt2,pt1)
            imgInvWarp = cv2.warpPerspective(imgRawDrawing,invMatrix,(widthImg,heightImg))

            #DISPLAY GRADES (Based on original image)
            imgRawGrade = np.zeros_like(imgGradeDisplay)
            cv2.putText(imgRawGrade,str(int(score))+"%",(80,80),cv2.LINE_AA,3,(0, 165, 255),3)

            #ALERT MESSAGE
            if 4 and 5 in grading:
                cv2.putText(imgRawGrade,"Alert: Duplicate shade",(30,110),cv2.LINE_AA,0.5,(255,255,255),1)
                cv2.putText(imgRawGrade,"Alert: Unshaded bubble",(30,135),cv2.LINE_AA,0.5,(255,255,255),1)
            elif 4 in grading:
                cv2.putText(imgRawGrade,"Alert: Duplicate shade",(30,130),cv2.LINE_AA,0.8,(255,255,255),1)
            elif 5 in grading:
                cv2.putText(imgRawGrade,"Alert: Unshaded bubble",(20,130),cv2.LINE_AA,0.8,(255,255,255),1)

            # cv2.imshow("Grade",imgRawGrade)

            #DISPLAY FINAL RESULTS (Based on original image)
            invMatrixG = cv2.getPerspectiveTransform(ptGrade2,ptGrade1)
            imgInvGradeDisplay = cv2.warpPerspective(imgRawGrade, invMatrixG, (widthImg,heightImg))
            imgFinal = cv2.addWeighted(imgFinal,0.25,imgInvWarp,1,0)
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

   # imgStacked = utility.stackImages(imageArray, 0.4, labels)

    # cv2.namedWindow("Stacked Images", cv2.WINDOW_NORMAL)    # Enables a resizable window
    # cv2.imshow("Stacked Images",imgStacked)


    # # 8. DISPLAY FINAL IMAGE
    # cv2.namedWindows("Final Image",cv2.WINDOW_NORMAL)
    fileName = "Graded_OMR" + time.strftime("%Y%m%d-%H%M%S", time.localtime()) + ".png"
    gradedOMRFileName = "graded/" + fileName
   # cv2.imshow("Final Image", imgFinal)                     # Display finalized image
    cv2.imwrite(gradedOMRFileName, imgFinal)                 # Save finalized image
    cv2.waitKey(0)
    return {"gradedOMRFileName": fileName, "score": score}

