from flask import Flask, render_template, request

app =Flask(__name__)

@app.route("/")
def home ():
    return render_template("add.html")
@app.route("/add", methods=["post", "get"])
def add():
    a =request.form.get("a", 2)
    b =request.form.get("a", 2)
    a=int(a)
    b=int(b)

    
    result = a + b

    return render_template("result.html", result=result)



if __name__ == "__main__":
    app.run( port = 4200, debug=True)
