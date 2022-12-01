from paddleocr import PaddleOCR, draw_ocr
import os
# 显示结果
from PIL import Image
import time
import re

def getText(imgPath):
    os.environ['KMP_DUPLICATE_LIB_OK']='True'
    ocr = PaddleOCR(lang='en')  # need to run only once to download and load model into memory
    result = ocr.ocr(imgPath, cls=True)
    # for idx in range(len(result)):
    #     res = result[idx]
    #     for line in res:
    #         print(line)

    result = result[0]
    image = Image.open(imgPath).convert('RGB')
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result]
    im_show = draw_ocr(image, boxes, txts, scores, font_path='../doc/fonts/simfang.ttf')
    im_show = Image.fromarray(im_show)
    fileName = 'result/result_'+time.strftime("%Y%m%d-%H%M%S", time.localtime())+'.jpg'
    im_show.save(fileName)

    student = {
        "studentName": "",
        "studentId": "",
        "studentSubject": "",
        "studentCourse":"",
        "textImg": fileName
    }

    for txt in txts:
        #check if txt equals 'Student Id:'
        if txt == 'Student Id:':
            # pattern = first is letter, then 4 digits
            pattern = re.compile(r'[A-Z]\d{4}')

            if(re.match(pattern,txts[txts.index(txt)+1], flags=0) != None):
                student["studentId"] = txts[txts.index(txt) + 1]
            else:
                student["studentId"] = ""

        #check if txt equals 'Student Name:'
        if txt == 'Name:':
            # pattern = check is name
            student["studentName"] = txts[txts.index(txt)+1]

        #check if txt equals 'Subject:'
        if txt == 'Subject:':
            # pattern = check is subject
            student["studentSubject"] = txts[txts.index(txt)+1]

        #check if txt equals 'Course:'
        if txt == 'Course:':
            # pattern = check is course
            student["studentCourse"] = txts[txts.index(txt)+1]

        print(txt)

    return student



