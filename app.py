from flask import Flask, request, jsonify, render_template, url_for
import pickle

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
