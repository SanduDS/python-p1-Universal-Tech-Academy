from application import app, db
from flask import flash, redirect, render_template, request, Response, json, url_for, session
from application.forms import LoginForm, RegisterForm
from application.models import User, Course, Enrollment
from mongoengine.errors import ValidationError, NotUniqueError

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", login = True)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if session.get('userName'):
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.objects(email=email).first()
        if user and user.get_password(password):
            session['user_id'] = user.user_id
            session['userName'] = user.first_name
            flash(f"{user.first_name}, Successfully Logged In!", "success")
            return redirect("/index")
        else:
            flash("Something went wrong", "danger")
    return render_template("login.html", form=form, login = True)

@app.route("/logout")
def logout(): 
    session.clear()
    return redirect(url_for('index'))

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if session.get('userName'):
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.objects.count()
        user_id += 1
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        user = User(user_id = user_id, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        try:
            user.save()
            flash("You are registered", "success")
        except NotUniqueError as e:
            flash(f"Error: {str(e)}", "danger")
    return render_template("register.html",title="Register", form=form, login = True)

@app.route("/courses")
@app.route("/courses/")
@app.route("/courses/<term>")
def courses(term="None"):
    if term is None:
        term = "Spring 2019"
    classes = Course.objects.order_by("+courseID")
    return render_template("courses.html", courseData=classes, term=term)


@app.route("/enrollment", methods=["GET", "POST"])
def enrollment():
    if not session.get('userName'):
        return redirect(url_for('login'))
    courseID = request.form.get("courseID")
    courseTitle= request.form.get("title")
    user_id = session.get('user_id')
    if courseID:
        if Enrollment.objects(user_id=user_id, courseID = courseID):
            flash(f"Already Registered {courseTitle}", "danger")
            return redirect(url_for("courses"))
        else:
            enrollment = Enrollment(user_id=user_id, courseID=courseID)
            enrollment.save()
            flash(f"Now Registered {courseTitle}", "success")

    classes = list( User.objects.aggregate(*[
            {
                '$lookup': {
                    'from': 'enrollment', 
                    'localField': 'user_id', 
                    'foreignField': 'user_id', 
                    'as': 'r1'
                }
            }, {
                '$unwind': {
                    'path': '$r1', 
                    'includeArrayIndex': 'r1_id', 
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$lookup': {
                    'from': 'course', 
                    'localField': 'r1.courseID', 
                    'foreignField': 'courseID', 
                    'as': 'r2'
                }
            }, {
                '$unwind': {
                    'path': '$r2', 
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$match': {
                    'user_id': user_id
                }
            }, {
                '$sort': {
                    'courseID': 1
                }
            }
        ]))

    return render_template("enrollment.html", enrollment = True, title = "Enrollment", classes=classes)

@app.route("/api/")
@app.route("/api/<idx>")
def api(idx=None):
    if(idx==None):
        jdata = Course.objects.all()
    else:
        jdata =  User.objects(courseID=idx).first()
    return Response(json.dumps(jdata), mimetype="application/json")

@app.route("/user")
def user():
    #User(user_id=1, first_name="Dhanushka", last_name="Sandaruwan", email="me@gamil.com", password="12345").save()
    users = User.objects.all()
    return render_template("user.html", users=users)