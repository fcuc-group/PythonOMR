from flask import Flask, flash, request, redirect, url_for, render_template
import process
import answerSheet
from flask_cors import CORS
from pyzbar.pyzbar import decode
from PIL import Image
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
    print(studentDetails)

    print(subjectId)
    print(studentName)
    print(studentId)
    print(answerList)



    #graded = process.process(data.url, answerList)
    statue = False



    # if(graded != None):
    #     statue = True

        #prcoess name

        #process qr

    return {"success":True,
            "gradedFile":"c:///.png",
            "processNameFile":"",
            "score":30,
            "studentName":"",
            "studentId":"",
            "subject":"",
            "course":""}


@app.route('/answerSheet', methods=['POST'])
def create_answerSheet():
    print(request.json)
    data = request.json
    path = answerSheet.createPDF(data['subjectId'], data['studentName'], data['studentId'], data['answerList'])
    return path


if __name__ == "__main__":
    app.run(debug=True)

