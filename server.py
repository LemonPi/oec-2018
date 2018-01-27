from flask import Flask
app = Flask(__name__)

app.debug = True

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
