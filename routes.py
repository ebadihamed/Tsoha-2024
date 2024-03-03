from app import app
from flask import render_template, request, redirect, session
import functions
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
from os import abort
@app.route("/")
def index():
    # Getting blogs from database and rendering it
    blogs = functions.get_blogs()
    return render_template("index.html", blogs=blogs)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        # Getting the credentials 
        username = request.form["uname"]
        password = request.form["password"]

        # Checking the credentials
        if len(username) == 0  or len(password) == 0:
            return render_template("error.html", message="fill all the empty spots")
        if len(username) > 50 or len(username) < 3:
            return render_template("error.html", message="username is too long or short")
        if len(password) > 50 or len(password) < 3:
            return render_template("error.html", message="password is too long or short")

        # Getting the credentials from the database
        user = functions.get_users(username)

        # If user is not in the database, then raises alert
        if not user:
            return render_template("error.html", message="user is not found")


        # If user exists then checks the password and Logs in
        else:
            user_id = user[0]
            result = functions.get_credentials(user_id)
            password_hash = result[0].password_hash

            if check_password_hash(password_hash, password):
                session["username"] = username
                session["user_id"] = user_id
                session["csrf_token"] = secrets.token_hex(16)

            else:
                return render_template("error.html", message="password is incorrect")


        return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        # Getting the credentials
        firstname = request.form['fname']
        username = request.form['uname']
        password = request.form['password']
        password_1 = request.form['password_1']
        password_hash = generate_password_hash(password)

        # Checking if the credentials are correct
        if len(firstname) > 50 or len(username) > 50:
            return render_template("error.html", error="firstname or username is too long")
        if password != password_1:
            return render_template("error.html", error="passwords do not match")
        if len(firstname) == 0 or len(username) == 0 or len(password) == 0 or len(password_1) == 0:
            return render_template("error.html", error="Fill all the empty spots")
        if len(password) < 3 or len(password) > 50:
            return render_template("error.html", error="password is too short or long")


        # Checking if the username already exists in the database
        user = functions.get_users(username)

        # If such user exists in the database, then alert the user
        if user:
            return render_template("error.html", message="username already exists")

        # If user is not in the database then we can create new one
        if not user:
            if password == password_1:
                functions.new_user(username, firstname, password_hash)
            else:
                return render_template("error.html", message="Passwords does not match")
        return render_template("login.html")

@app.route("/log_out")
def log_out():
    del session["username"]
    return redirect("/")

@app.route("/new_blog", methods=["GET", "POST"])
def new_blog():
    if request.method == "GET":
        return render_template("new.html")
    
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        # Get the content from POST and user_id from the database
        username = session["username"]
        content = request.form['content']

        # Check the content
        if len(content) == 0:
            return render_template("error.html", message="content is empty")
        if len(content) < 5 or len(content) > 250:
            return render_template("error.html", message="content is too long or too short")
        
        result = functions.get_users(username)
        user_id = result[0]

        # Send the content and additional information to the database to be saved
        functions.new_blog(content, user_id)

        return redirect("/")

@app.route("/like", methods=["POST"])
def like():
    # Get the blog_id from POST and user_id from database
    blog_id = request.form["blog_id"]
    user_id = request.form["user_id"]
    username = session["username"]
    result = functions.get_users(username)
    user_id = result[0]

    # Checks if the user has liked the blog before
    if functions.check_like(user_id, blog_id):
        # Insert the like to the database and redirect to main page
        functions.like(user_id, blog_id)

    return redirect("/")

@app.route("/edit", methods =["POST"])
def edit():
    blog_id = request.form["blog_id"]
    result = functions.get_content(blog_id)
    content = result[0]
    return render_template("edit.html", content=content, id=blog_id)

@app.route("/cancel", methods=["POST"])
def cancel():
    return redirect("/")

@app.route("/edit_save", methods=["POST"])
def edit_save():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    
    # Get the content and 
    content = request.form["content"]
    blog_id = request.form["id"]

    # Update the database with new content
    functions.update_blog(content, blog_id)

    return redirect("/")

@app.route("/remove", methods=["POST"])
def remove():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    blog_id = request.form["blog_id"]
    functions.remove_blog(blog_id)
    return redirect("/")