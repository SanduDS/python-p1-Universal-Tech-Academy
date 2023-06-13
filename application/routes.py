from application import app, db
from flask import render_template, request, Response, json

coursesData = [{"courseID":"1111","title":"PHP 101","description":"Intro to PHP","credits":3,"term":"Fall, Spring"}, {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":4,"term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":3,"term":"Fall"}, {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":3,"term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":4,"term":"Fall"}]

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", login = True)

@app.route("/courses")
@app.route("/courses/")
@app.route("/courses/<term>")
def courses(term="Spring 2019"):
    return render_template("courses.html", courseData=coursesData, term=term)

@app.route("/enrollment", methods=["GET", "POST"])
def enrollment():
    id= request.form.get("courseID")
    title= request.form["title"]
    term= request.form.get("term")
    return render_template("enrollment.html", enrollment = True, data={"id":id, "title":title, "term":term})

@app.route("/api/")
@app.route("/api/<idx>")
def api(idx=None):
    if(idx==None):
        jdata = coursesData
    else:
        jdata = coursesData[int(idx)]
    return Response(json.dumps(jdata), mimetype="application/json")

class User(db.Document):
    user_id     =   db.IntField( unique=True)
    first_name  =   db.StringField ( max_length =50 )
    last_name   =   db.StringField ( max_length =50 )
    email       =   db.StringField ( max_length =30 )
    password    =   db.StringField ( max_length =30 )

@app.route("/user")
def user():
    #User(user_id=1, first_name="Dhanushka", last_name="Sandaruwan", email="me@gamil.com", password="12345").save()
    users = User.objects.all()
    return render_template("user.html", users=users)