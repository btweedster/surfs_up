from flask import Flask

app = Flask(__name__)

@app.route('/')

def hello_world():
    return 'Hello world'

# Had to add the following for the app to work
if __name__ == '__main__':
    app.run(debug=True)