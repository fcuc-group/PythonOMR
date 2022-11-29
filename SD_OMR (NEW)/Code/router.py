from flask import Flask, flash, request, redirect, url_for, render_template
import process
import answerSheet
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return "Hello World"

@app.route('/upload_image', methods=['POST'])
def upload_image():

    print(request.json)
    data = request.json
    graded = process.process(data.url, data.answer)
    statue = False
    if(graded != None):
        statue = True

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
    path = answerSheet.createPDF(data['subjectId'], data['studentName'], data['studentId'])
    return path


if __name__ == "__main__":
    app.run(debug=True)

