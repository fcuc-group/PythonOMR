from flask import Flask, flash, request, redirect, url_for, render_template
import process
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

    return {"success":statue,
            "gradedFile":graded.gradedOMRFileName,
            "processNameFile":"",
            "score":graded.score,
            "studentName":"",
            "studentId":"",
            "subject":"",
            "course":""}


if __name__ == "__main__":
    app.run(debug=True)

