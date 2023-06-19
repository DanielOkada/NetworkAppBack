from flask import *
import pandas as pd
import network
import secrets
import os

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def index():
    if "user_key" not in session:
        session["user_key"] = secrets.token_hex()
    return render_template("index.html", upload=url_for("upload"), test=url_for("get_file_name"))


@app.route('/upload', methods=['POST'])
def upload():
    if "user_key" not in session:
        session["user_key"] = secrets.token_hex()
    file = request.files['file']

    session["filename"] = file.filename
    print(file.filename)
    file_path = f'uploads/{session["user_key"]}/'
    os.makedirs(file_path, exist_ok=True)
    file.save(file_path + session["filename"])

    session["file_path"] = file_path

    return {"status": "success"}


@app.route('/get_network')
def get_network():
    input_book = pd.ExcelFile(session["file_path"] + session["filename"])
    json = network.get_network_image(input_book, session["sheet"])
    # print(json)
    return json


@app.route('/get_file_name')
def get_file_name():
    return session["filename"]


@app.route('/get_sheets')
def get_sheets():
    print(session["file_path"] + session["filename"])
    input_book = pd.ExcelFile(session["file_path"] + session["filename"])
    return {"sheets": input_book.sheet_names}


@app.route('/set_sheet', methods=["POST"])
def set_sheet():
    session["sheet"] = request.form["sheet"]
    print(session["sheet"])
    return {"status": "success"}


@app.route('/test')
def test():
    return {"test": "tesuto desu"}


if __name__ == '__main__':
    app.run(debug=True)
