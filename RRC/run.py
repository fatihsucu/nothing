from flask import Flask
from flask import render_template



app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html', lat=41.040, lng=29.0236111)


if __name__ == "__main__":
    app.run("192.168.33.10", debug=True)
