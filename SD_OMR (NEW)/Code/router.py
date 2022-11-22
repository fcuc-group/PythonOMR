from flask import Flask, flash, request, redirect, url_for, render_template
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World"

@app.route('/upload_image', methods=['POST'])
def upload_image():

    print(request.json)

    return {"success":"true","processedFile":"c:/xxxx"};

if __name__ == "__main__":
    app.run(debug=True)

