from flask import Flask, flash, request, redirect, url_for, render_template
import process
import grade
import editScore
import answerSheet
from flask_cors import CORS
from pyzbar.pyzbar import decode
from PIL import Image
import getText
app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return "Hello World"

@app.route('/upload_image', methods=['POST'])
def upload_image():

    print(request.json)
    data = request.json

    if data['url'] is None:
        return "No url"

    # QR Code
    decocdeQR = decode(Image.open(data['url']))       #change path
    studentDetails = decocdeQR[0].data.decode('ascii')

    # sp studentDetails with comma
    studentDetails = studentDetails.split(';')
    subjectId = studentDetails[0]
    studentName = studentDetails[1]
    studentId = studentDetails[2]
    answerList = studentDetails[3].split(',')
    #for lop to convert string to int
    for i in range(len(answerList)):
        answerList[i] = int(answerList[i])

    print(studentDetails)
    print(subjectId)
    print(studentName)
    print(studentId)
    print(answerList)

    #answerList = [1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4]

    student = getText.getText(data['url'])


    graded = grade.grade(data['url'], answerList)
    print(graded)
    statue = False



    if(graded != None):
        statue = True

        #prcoess name

        #process qr
    # path = "E:/FCUC/PythonOMR/SD_OMR (NEW)/Code/"


    return {"success":statue,
            "gradedFile":graded['gradedOMRFileName'],
            "processNameFile":student['textImg'],
            "score":graded['score'],
            "studentName":student['studentName'],
            "studentId":student['studentId'],
            "subject":student['studentSubject'],
            "course":student['studentCourse']}


@app.route('/answerSheet', methods=['POST'])
def create_answerSheet():
    print(request.json)
    data = request.json
    path = answerSheet.createPDF(data['subjectId'], data['studentName'], data['studentId'], data['answerList'])
    return path


@app.route('/editScore', methods=['PUT'])
def edit_score():
    print(request.json)



if __name__ == "__main__":
    app.run(debug=True)

