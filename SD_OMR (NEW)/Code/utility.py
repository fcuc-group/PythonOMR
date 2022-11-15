# <editor-fold desc="FILE DESCRIPTION">
# DESCRIPTION :
#       This file contains all the function that will be called in grader.py
#
#  PUBLIC FUNCTIONS :
#       stackImages(), rectContours(), reorder(), splitBoxes(), getCornerPoints(), showAnswers()
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
import cv2
import numpy as np

# <editor-fold desc="USER-GUIDE">
# 1. Description       : This file contains all the function that will be called in grader.py
# 2. List of functions : stackImages, rectContours, reorder, splitBoxes, getCornerPoints, showAnswers
# </editor-fold>

# <editor-fold desc="1. STACK ALL IMAGES IN ONE WINDOW (PRE-DEFINED LOGIC)">
# 1. Parameters     :
    # • imgArray , Array of images
    # • scale    , Image scale
    # • lables   , Image label
# 2. Return value:
    # • ver      , Image stack
# </editor-fold>
def stackImages(imgArray,scale,lables=[]):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        hor_con= np.concatenate(imgArray)
        ver = hor
    if len(lables) != 0:
        eachImgWidth= int(ver.shape[1] / cols)
        eachImgHeight = int(ver.shape[0] / rows)
        #print(eachImgHeight)
        for d in range(0, rows):
            for c in range (0,cols):
                cv2.rectangle(ver,(c*eachImgWidth,eachImgHeight*d),(c*eachImgWidth+len(lables[d][c])*13+27,30+eachImgHeight*d),(255,255,255),cv2.FILLED)
                cv2.putText(ver,lables[d][c],(eachImgWidth*c+10,eachImgHeight*d+20),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),2)
    return ver

# <editor-fold desc="2. IDENTIFY ALL RECTANGLE CONTOURS">
# 1. Parameters     :
#    • contours  , rectangle contours
# 2. Return value:
#    • rectCont  , all rectangles contours are stored here
# </editor-fold>
def rectContour(contours):
    rectCon = []     #CREATE NEW LIST
    max_area = 0
    # 2.1. LOOP THROUGH ALL CONTOURS
    for i in contours:
        area = cv2.contourArea(i)
        # print(area) # CHECK CONTOUR AREA

        if area > 50:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            # print("Corner Points: ", len(approx))
            if len(approx) == 4:
                # print(i)
                rectCon.append(i)
                # print(rectCon)
    # 2.2. REORDER AND SORT RECTCON, BASED ON OMR FORM
    rectCon = sorted(rectCon, key=cv2.contourArea,reverse=True) # reverse=True, sort in descending order (biggest to smallest)
    # print(len(rectCon))
    return rectCon

# <editor-fold desc="3. TBA">
# 1. Parameters     :
    # • myPoints    , TBA
# 2. Return value:
    # • myPointsNew , TBA
# </editor-fold>
def reorder(myPoints):
    myPoints = myPoints.reshape(4, 2)
    myPointsNew = np.zeros((4, 1, 2), np.int32) # NEW MATRIX WITH ARRANGED POINTS
    add = myPoints.sum(1)
    # print(myPoints)
    # print(add)
    myPointsNew[0] = myPoints[np.argmin(add)]  #[0,0]
    # print(np.argmax(add))
    myPointsNew[3] =myPoints[np.argmax(add)]   #[w,h]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] =myPoints[np.argmin(diff)]  #[w,0]
    myPointsNew[2] = myPoints[np.argmax(diff)] #[h,0]
    # print(diff)
    return myPointsNew

# <editor-fold desc="4. SPLIT BUBBLES VERTICALLY INSIDE OF ANSWER ZONE">
# 1. Parameters     :
    # • img    , test_case zone image
# 2. Return value:
    # • boxes , the bubbles for each question
# </editor-fold>
def splitBoxes(img):

    rows = np.vsplit(img,20)     # 10, because there is 10 rows
    # cv2.imshow("Split",rows[0])

    # Split bubbles horizontally
    boxes=[]
    for r in rows:
        cols= np.hsplit(r,4)   # 4, because there is 4 questions per column
        for box in cols:
            boxes.append(box)
            # cv2.imshow("Split",box)
    return boxes

# <editor-fold desc="5. GET CORNER POINTS OF A CONTOUR">
# 1. Parameters     :
    # • cont    , test_case zone image
# 2. Return value:
    # • approx , the approximate value of a contour
# </editor-fold>
def getCornerPoints(cont):
    peri = cv2.arcLength(cont, True) # Length of contour
    approx = cv2.approxPolyDP(cont, 0.02 * peri, True) # Approximate the poly to get corner points
    return approx

# <editor-fold desc="6. DISPLAY ANSWERS">
# 1. Parameters     :
    # • img         , Bird's-eyes: test_case zone
    # • myIndex     , The index of the pre-defined test_case
    # • grading     , The graded question
    # • ans         , Pre-defined test_case
    # • questions   , Number of questions
    # • choices     , Number of choices
# 2. Return value:
    # • img         , Image of the graded paper
# </editor-fold>
# def showAnswers(img,myIndex,grading,ans,questions=5,choices=5): # (PRE-DEFINED DRIVER CODE)
def showAnswers(img,myIndex,grading,ans,questions,choices):

    # SIMULATE A 5*5 shape (based on test_case zone)
    sectWidth = int(img.shape[1]/questions)
    sectHeight = int(img.shape[0]/choices)

    for x in range(0,questions):
        myAns = myIndex[x]

        # c = center of position
        # cX = (myAns * sectWidth) + sectWidth #DEFAULT FORMAT
        # cY = (x * sectHeight) + sectHeight // 2 #DEFAULT FORMAT
        # print("cX=",cX," cY=",cY) #CHECK VALUES
        # print("Grading=",grading[x]) #CHECK VALUES

        cY = ((x * sectHeight)//5)+30

        if grading[x]==1:          # LOGIC: 1 correct test_case, 0 wrong test_case
            if myAns == 0:
                cX = (myAns * sectWidth) + sectWidth // 2 + 50  # DEFAULT FORMAT
                # cY = (x * sectWidth) +20
            elif myAns == 1:
                cX = (myAns * sectWidth) + sectWidth // 2 + 120  # DEFAULT FORMAT
                # cY = (x * sectWidth)+50
            elif myAns == 2:
                cX = (myAns * sectWidth) + sectWidth // 2 + 200  # DEFAULT FORMAT
                # cY = (x * sectWidth)+100
            elif myAns == 3:
                cX = (myAns * sectWidth) + sectWidth // 2 + 270  # DEFAULT FORMAT
                # cY = (x * sectWidth)+150

            myColor = (0,255,0)     # GREEN
            cv2.circle(img,(cX,cY),10,myColor,cv2.FILLED)  # Fill correct test_case in GREEN

        elif grading[x]==0:
            if myAns == 0:
                cX = (myAns * sectWidth) + sectWidth // 2 + 50    #DEFAULT FORMAT
            elif myAns == 1:
                cX = (myAns * sectWidth) + sectWidth // 2 + 120    #DEFAULT FORMAT
            elif myAns == 2:
                cX = (myAns * sectWidth) + sectWidth // 2 + 200   #DEFAULT FORMAT
            elif myAns == 3:
                cX = (myAns * sectWidth) + sectWidth // 2 + 270   #DEFAULT FORMAT

            myColor = (123, 24, 24)  # BLUE
            cv2.circle(img, (cX, cY), 10, myColor, cv2.FILLED)  # Fill correct test_case in BLUE

            correctAns = ans[x]
            if correctAns== 0:
                cX = (correctAns * sectWidth) + sectWidth // 2 + 50  # DEFAULT FORMAT
            elif correctAns== 1:
                cX = (correctAns* sectWidth) + sectWidth // 2 + 120  # DEFAULT FORMAT
            elif correctAns == 2:
                cX = (correctAns* sectWidth) + sectWidth // 2 + 200  # DEFAULT FORMAT
            elif correctAns == 3:
                cX = (correctAns* sectWidth) + sectWidth // 2 + 270  # DEFAULT FORMAT
            myColor = (0,255,0)     # GREEN
            cv2.circle(img, (cX, cY), 10, myColor, cv2.FILLED)  # Fill correct test_case in GREEN

    # cv2.imshow("Show Answers",img)
    return img


#Added: To check for more than 1 shaded bubble
# def check(_questionRow, val):
#     # traverse in the list
#     for x in list1:
#         # compare with all the values
#         # with val
#         if val>= x:
#             return False
#     return True