from db import db
from sqlalchemy.sql import text


def get_blogs():
    result = db.session.execute(text('SELECT b.id, b.content, b.created_at, b.user_id AS user_id, COUNT(i.id) AS likes FROM blogs b LEFT JOIN blog_likes i ON b.id = i.blog_id GROUP BY b.id, b.content, b.created_at ORDER BY b.created_at DESC'))
    blogs = result.fetchall()
    return blogs

def get_users(username):
    sql = text("SELECT id, username, name FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    return user

def get_credentials(user_id):
    sql = text("SELECT id, user_id, password_hash FROM credentials WHERE user_id=:user_id")
    result = db.session.execute(sql, {"user_id":user_id})
    credentials = result.fetchall()
    print(credentials)
    return credentials

def new_user(username, firstname, password_hash):
    sql = text("INSERT INTO users (username, name, created_at) VALUES (:username, :name, NOW()) RETURNING id")
    result = db.session.execute(sql, {"username":username ,"name":firstname})
    user_id = result.fetchone()[0]
    sql_1 = text("INSERT INTO credentials (user_id, password_hash, created_at) VALUES (:user_id, :password_hash, NOW())")
    db.session.execute(sql_1, {"user_id":user_id, "password_hash":password_hash})
    db.session.commit()

def new_blog(content, user_id):
    sql = text("INSERT INTO blogs (content, user_id, created_at) VALUES (:content, :user_id, NOW())")
    db.session.execute(sql, {"content":content, "user_id":user_id})
    db.session.commit()

def like(user_id, blog_id):
    sql = text("INSERT INTO blog_likes (user_id, blog_id, created_at) VALUES (:user_id, :blog_id, NOW())")
    db.session.execute(sql, {"user_id": user_id, "blog_id": blog_id})
    db.session.commit()

def get_content(blog_id):
    sql = text("SELECT content FROM blogs WHERE id=:blog_id")
    result = db.session.execute(sql, {"blog_id": blog_id})
    content = result.fetchone()
    return content

def update_blog(content, blog_id):
    sql = text("UPDATE blogs SET content = :content WHERE id = :blog_id")
    db.session.execute(sql, {"content": content, "blog_id": blog_id})
    db.session.commit()