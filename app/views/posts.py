from flask import Blueprint, redirect, url_for, request, render_template, session
from app.models import Posts, db, Users

post_bp = Blueprint("posts", __name__)

@post_bp.route("/create-posts")
def index(): 
    return render_template("index.html")

@post_bp.route("/home",methods=["POST"])
def home_page(): 
    form_data= request.form.to_dict()
    current_user = Users.query.filter_by(username = session["username"]).first()
    new_post = Posts(title = form_data["title"], description= form_data["description"], username=current_user.username)
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for('posts.get_posts'))
        

@post_bp.route("/posts", methods = ["GET"])
def get_posts():
    if "username" in session:
        post = Posts.query.all()
        username = session["username"]
        return render_template("home.html", posts= post, user = username)
    else:
        return redirect(url_for("auth.login"))

@post_bp.route("/posts/<int:id>", methods=["GET"])
def get_post_by_id(id): 
    post = Posts.query.get_or_404(id)
    return {"id" : post.id,
            "title" : post.title,
            "description" : post.description,
            "posted_time" : post.time}

