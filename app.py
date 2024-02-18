from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
    result = db.session.execute(text('SELECT b.id, b.content, b.created_at, b.user_id AS user_id, COUNT(i.id) AS likes FROM blogs b LEFT JOIN blog_likes i ON b.id = i.blog_id GROUP BY b.id, b.content, b.created_at ORDER BY b.created_at DESC'))
    blogs = result.fetchall()
    return render_template("index.html", blogs=blogs)

@app.route("/sign_in")
def sign_in():
    return render_template("sign_in.html")

@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")

@app.route("/log_in", methods=["POST"])
def log_in():
    # Getting the credentials
    username = request.form["uname"]
    password = request.form["password"]

    # Getting the credentials from the database
    sql = text("SELECT id, username, name FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()

    # If user is not in the database, then raises alert
    if not user:
        print("user not found")

    # If user exists then checks the password and Logs in
    else:
        user_id = user[0]
        sql_1 = text("SELECT id, user_id, password_hash FROM credentials WHERE user_id=:user_id")
        result_1 = db.session.execute(sql_1, {"user_id":user_id})
        password_hash = result_1.fetchone()[2]

        if check_password_hash(password_hash, password):
            session["username"] = username
            session["user_id"] = user_id
            print("logged in")

        else:
            print("invalid password")

    return redirect("/")

@app.route("/new_account", methods=["POST"])
def new_account():
    # Getting the credentials
    fullname = request.form['fname']
    username = request.form['uname']
    password = request.form['password']
    password_hash = generate_password_hash(password)

    # Checking if the username already exists in the database
    sql = text("SELECT id, username, name FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()

    # If such user exists in the database, then alert the user
    if user:
        pass

    # If user is not in the database then we can create new one
    if not user:
        sql_1 = text("INSERT INTO users (username, name, created_at) VALUES (:username, :name, NOW()) RETURNING id")
        result_1 = db.session.execute(sql_1, {"username":username ,"name":fullname})
        user_id = result_1.fetchone()[0]
        sql_2 = text("INSERT INTO credentials (user_id, password_hash, created_at) VALUES (:user_id, :password_hash, NOW())")
        result_2 = db.session.execute(sql_2, {"user_id":user_id, "password_hash":password_hash})
        db.session.commit()
    return redirect("/sign_in")

@app.route("/log_out")
def log_out():
    del session["username"]
    return redirect("/")

@app.route("/new_blog")
def new_blog():
    return render_template("new.html")

@app.route("/create", methods=["POST"])
def create():
    # Get the content from POST and user_id from the database
    user = session["username"]
    content = request.form['content']
    sql = text("SELECT id FROM users WHERE username = :user")
    result = db.session.execute(sql, {"user":user})
    user_id = result.fetchone()[0]

    # Send the content and additional information to the database to be saved
    sql_1 = text("INSERT INTO blogs (content, user_id, created_at) VALUES (:content, :user_id, NOW())")
    result_1 = db.session.execute(sql_1, {"content":content, "user_id":user_id})
    db.session.commit()
    return redirect("/")

@app.route("/like", methods=["POST"])
def like():
    # Get the blog_id from POST and user_id from database
    blog_id = request.form["blog_id"]
    username = session["username"]
    sql = text("SELECT id FROM users WHERE username = :username")
    result = db.session.execute(sql, {"username": username})
    user_id = result.fetchone()[0]

    # Insert the like to the database and redirect to main page
    sql_1 = text("INSERT INTO blog_likes (user_id, blog_id, created_at) VALUES (:user_id, :blog_id, NOW())")
    result_1 = db.session.execute(sql_1, {"user_id": user_id, "blog_id": blog_id})
    db.session.commit()
    return redirect("/")

@app.route("/edit", methods =["POST"])
def edit():
    blog_id = request.form["blog_id"]
    sql = text("SELECT content FROM blogs WHERE id=:blog_id")
    result = db.session.execute(sql, {"blog_id": blog_id})
    content = result.fetchone()[0]
    return render_template("edit.html", content=content, id=blog_id)

@app.route("/edit_cancel", methods=["POST"])
def edit_cancel():
    return redirect("/")

@app.route("/edit_save", methods=["POST"])
def edit_save():
    # Get the content and 
    content = request.form["content"]
    blog_id = request.form["id"]

    # Update the database with new content
    sql = text("UPDATE blogs SET content = :content WHERE id = :blog_id")
    result = db.session.execute(sql, {"content": content, "blog_id": blog_id})

    db.session.commit()
    return redirect("/")