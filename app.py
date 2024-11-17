from flask import Flask, jsonify, request
from http import HTTPStatus

app = Flask(__name__)


@app.route('/')
def hello_word():
    return "Hello Word"



if __name__ == "__main__":
    app.run(debug=True)