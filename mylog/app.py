from flask import Flask, render_template, request, make_response, session, redirect
import hashlib
from article import Article
import os

app = Flask(__name__)
app.secret_key = "thisissecretkey"


users = {
    "admin": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
}

articles =Article.all()





@app.route("/")
def home():
    return render_template("blog.html", articles =articles)

@app.route("/blog/<slug>")
def article(slug: str):
    article = articles.get(slug)
    return render_template("article.html", article =article)


@app.route("/first-time")
def first_time():
    render_template ("login.html")
    if 'seen' not in request.cookies:
        response = make_response("You are new here")
        response.set_cookie('seen', "1")
        return response
    
    return "I have seen you before"

@app.route("/set-session")
def set_session():
    session["user_id"] =1
    return "Session o'rnatildi"

@app.route("/get-session")
def get_session():
    return f"user_id {session["user_id"]}"
    

@app.get("/admin")
def login():
     if "user" in session:
         return "ro'yhatdan allaqachon o'tib bo'lgansiz."
     return render_template ("login.html")

@app.post("/admin")
def admin_login():
    username =request.form.get('username')
    password = request.form.get('password')

    if username not in users:
        return render_template("login.html", error="username/password xato")
    
    hashedPass = hashlib.sha256(password.encode()).hexdigest()
    
    if users[username] != hashedPass:
        return render_template("login.html", error="username/password xato")
    
    session["user"] = username
    return "Siz ro'yhatdan o'tdingiz"

@app.get("/log-out")
def logout():
    del session['user']
    return "Siz chiqib ketdingiz"


@app.get("/publish")
def publish():
    if "user" not in session:
        return redirect("/admin")
    return render_template("publish.html")

ARTICLES_DIR = "articles"
if not os.path.exists(ARTICLES_DIR):
    os.makedirs(ARTICLES_DIR)


@app.route("/post", methods=["GET", "POST"])
def uy():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("matn", "").strip()

        if title and content:
            filename = f"articles/{title.replace(' ', '_')}.md"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"# {title}\n\n{content}")

            return "Article Published Successfully!"

    return render_template("publish.html")



if __name__ == "__main__":
    app.run(debug=True)