#!/usr/bin/python3

from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)


UPLOAD_FOLDER = 'File'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# allowed extension
ALLOWED_EXTENSIONS = {'log'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return send_from_directory('webpage','index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    
    # Check if the POST request has the file part
    if 'file' not in request.files:   
        return 'No file part'
    file = request.files['file']
    
    
    # if no file is selected
    if file.filename == '':    
        return 'No selected file'
    

    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return f'File successfully uploaded to {filepath}'
    else:
        return 'File type not allowed'


if __name__ == "__main__":
    app.run()  # debug = False
