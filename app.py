from flask import Flask
import pickle

app = Flask(__name__)



@app.route('/hello')
def hello_world():  # put application's code here
    return 'hello'


if __name__ == '__main__':
    app.run()
