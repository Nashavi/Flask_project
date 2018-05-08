from flask import Flask, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('mssql+pyodbc://(LocalDb)\MSSQLLocalDB/Migratedb?driver=SQL+Server+Native+Client+11.0')
db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

@app.route('/')
def landing():
    return render_template("landing.html")

@app.route('/home',methods = ["POST"])
def home():
    name = request.form.get("name")
    return render_template('home.html',name = name)

@app.route('/viewDB',methods = ["GET","POST"])
def viewDB():
    jobtitles = db.execute("SELECT DISTINCT(JOB_TITLE) from HR1.JOBS").fetchall()
    db.commit()
    if request.method == "GET":
        return render_template("viewdb_jtitles.html", results=jobtitles, salaries=[])
    if request.method == "POST":
        jtitle = request.form["job_title"]
        salaries = db.execute("SELECT * from HR1.JOBS where JOBS.JOB_TITLE = :JTLE",{"JTLE":jtitle}).fetchall()
        db.commit()
    return render_template("viewdb_jtitles.html",results=jobtitles, salaries=salaries)

@app.route('/postSalary',methods = ["POST"])
def postSalary():
        return render_template("poster.html")

@app.route('/posted',methods = ["POST"])
def posted():
    jobtitle = request.form.get("poster job")
    try:
        minsalary = request.form.get("min salary")
    except ValueError:
        return render_template("error.html",message="Invalid Minimum Salary")
    try:
        maxsalary = request.form.get("max salary")
    except ValueError:
        return render_template("error.html",message="Invalid Maximum Salary")
    if len(jobtitle.split()) > 1 :
        jobid = jobtitle[:2].upper()+"_"+jobtitle.split()[1][:3].upper()
    else:
        jobid = jobtitle[:5].upper()

    if db.execute("SELECT COUNT(*) FROM HR1.JOBS WHERE JOB_ID = :jid",{"jid":jobid}).rowcount != 0:
        return render_template("error.html", message="Salary Exists already")

    # existing_rows = db.execute("SELECT COUNT(*) FROM HR1.JOBS WHERE JOB_ID = :jid",{"jid":jobid}).scalar()
    # if existing_rows == 1:
    #     jobid = jobid + "1"
    # elif existing_rows > 1:
    #     jobid = jobid[:-1] + str(int(jobid[-1])+1)

    db.execute("INSERT INTO HR1.JOBS(JOB_ID,JOB_TITLE,MIN_SALARY,MAX_SALARY) VALUES(:JOB_ID,:JOB_TITLE,:MIN_SALARY,:MAX_SALARY)",
               {"JOB_ID":jobid,"JOB_TITLE":jobtitle,"MIN_SALARY":minsalary,"MAX_SALARY":maxsalary})
    db.commit()

    return render_template("success.html", message="Salary successfully posted")

if __name__ == '__main__':
    app.run(debug=True)