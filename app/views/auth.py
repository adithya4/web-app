from flask import Blueprint, request, render_template, redirect, url_for, session
from app.models import Users, db
from app.hash import hash, password_verify

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/sign-in")
def sign_in():
    return render_template("sign_in.html")

@auth_bp.route("/sign-in-verify", methods=["POST"])
def verify():
    username = request.form["username"]
    password = request.form["password"]
    try:
        hashed_password = hash(password)
        user = Users(username= username, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        print(f'username : {username}, password : {password}')
    except Exception as e:
        return str(e)
    return redirect(url_for("posts.get_posts"))


@auth_bp.route("/login")
def login():
    return render_template("login.html")

@auth_bp.route("/login-verify", methods=["POST","GET"])
def login_verify():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
    
        no_of_users = db.session.query(Users).all()
        for user in no_of_users:
            if username == user.username and password_verify(password, user.password):
                session.permanent = True
                session["username"] = username
                return redirect(url_for("posts.get_posts"))
    
        else:
            return redirect(url_for("auth.login"))

    else:
        if "username" in session:
            return redirect(url_for("posts.get_posts"))
        else:
            return redirect(url_for("auth.login"))
        
@auth_bp.route("/logout")
def logout():
    if "username" in session:
        session.pop("username")
    return redirect(url_for("auth.login"))

