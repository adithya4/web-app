from flask import Blueprint, request, send_file, render_template, redirect, url_for, session
from app.models import Users, db
from app.hash import hash, password_verify
import io, base64

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
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


@auth_bp.route("/login",methods=["POST","GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
    
        no_of_users = db.session.query(Users).all()
        for user in no_of_users:
            if username == user.username and password_verify(password, user.password):
                session.permanent = True
                session["username"] = username
                return redirect(url_for("posts.get_posts"))
    
        else:
            return render_template("login.html")
        
@auth_bp.route("/account", methods=["POST","GET"])
def account():
    if request.method == "POST":
        current_user = Users.query.filter_by(username = session["username"]).first()
        img = request.files['image'].read()
        encoded_img = base64.b64encode(img)
        current_user.image = encoded_img
        db.session.commit()
        return render_template("account.html",user=current_user)
    else:
        if "username" in session:
            current_user = Users.query.filter_by(username = session["username"]).first()            
            return render_template("account.html",user = current_user)
        return render_template("login.html")

@auth_bp.route("/user-profile-pic")
def get_img():
    current_user = Users.query.filter_by(username = session["username"]).first()
    return send_file(io.BytesIO(current_user.image), mimetype="image/jpeg")

@auth_bp.route("/images")
def im():
    current_user = Users.query.filter_by(username = session["username"]).first() 
    return str(current_user.image)

@auth_bp.route("/logout", methods=["POST"])
def logout():
     if "username" in session:
        session.pop("username")
        return redirect(url_for("auth.login"))
     else:
         return redirect(url_for("auth.login"))