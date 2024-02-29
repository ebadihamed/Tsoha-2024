from app import app
from flask import render_template, request, redirect, session
import functions
from werkzeug.security import check_password_hash, generate_password_hash

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

        # Getting the credentials from the database
        user = functions.get_users(username)

        # If user is not in the database, then raises alert
        if not user:
            print("user not found")

        # If user exists then checks the password and Logs in
        else:
            user_id = user[0]
            result = functions.get_credentials(user_id)
            password_hash = result[0].password_hash

            if check_password_hash(password_hash, password):
                session["username"] = username
                session["user_id"] = user_id
                print("logged in")

            else:
                print("invalid password")

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

        # Checking if the username already exists in the database
        user = functions.get_users(username)

        # If such user exists in the database, then alert the user
        if user:
            pass

        # If user is not in the database then we can create new one
        if not user:
            if password == password_1:
                functions.new_user(username, firstname, password_hash)
            else:
                print("incorrect password")
        return redirect("/")

@app.route("/log_out")
def log_out():
    del session["username"]
    return redirect("/")

@app.route("/new_blog", methods=["GET", "POST"])
def new_blog():
    if request.method == "GET":
        return render_template("new.html")
    
    if request.method == "POST":
        # Get the content from POST and user_id from the database
        username = session["username"]
        content = request.form['content']
        result = functions.get_users(username)
        print(result)
        user_id = result[0]

        # Send the content and additional information to the database to be saved
        functions.new_blog(content, user_id)

        return redirect("/")

@app.route("/like", methods=["POST"])
def like():
    # Get the blog_id from POST and user_id from database
    blog_id = request.form["blog_id"]
    username = session["username"]
    result = functions.get_users(username)
    print(result)
    user_id = result[0]

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
    # Get the content and 
    content = request.form["content"]
    blog_id = request.form["id"]

    # Update the database with new content
    functions.update_blog(content, blog_id)

    return redirect("/")