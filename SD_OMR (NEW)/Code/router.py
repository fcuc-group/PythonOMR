from flask import Flask, flash, request, redirect, url_for, render_template
import process
app = Flask(__name__)

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

