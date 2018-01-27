from flask import Flask, render_template
app = Flask(__name__)

app.debug = True

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
