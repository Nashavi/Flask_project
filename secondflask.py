from flask import Flask, render_template, request, session
from flask_session import Session

app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello, Flask'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

@app.route('/')
def landing():
    return render_template("landing.html")

@app.route('/home',methods = ["POST"])
def home():
    name = request.form.get("name")
    if session.get("posts") is None:
        session["posts"] = []
    else:
        post = request.form.get("post")
        session["posts"].append(post)
    return render_template('home.html',name = name, posts = session["posts"])

if __name__ == '__main__':
    app.run(debug=True)