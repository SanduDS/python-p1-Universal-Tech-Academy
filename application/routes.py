from application import app
from flask import render_template

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", login = True)

@app.route("/courses")
@app.route("/courses/")
@app.route("/courses/<term>")
def courses(term="Spring 2019"):
    coursesData = [{"courseID":"1111","title":"PHP 101","description":"Intro to PHP","credits":3,"term":"Fall, Spring"}, {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":4,"term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":3,"term":"Fall"}, {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":3,"term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":4,"term":"Fall"}]
    print(coursesData)
    return render_template("courses.html", courseData=coursesData, term=term)

@app.route("/")
@app.route("/enrollment")
def enrollment():
    return render_template("index.html", login = True)