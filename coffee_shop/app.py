from flask import *
import sqlite3 as sq
import os

app=Flask(__name__)
upload_folder='C:/Users/user/Desktop/coffee_shop/static/images'

app.config['upload_folder']=upload_folder
app.secret_key="india@11"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/menu")
def galley():
    return render_template("menu.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/reg")
def reg():
    return render_template("reg.html")

@app.route("/formsave",methods=["GET","POST"])
def formsave():
    if request.method=="POST":
        fn=request.form["name"]
        em=request.form["email"]
        ps=request.form["password"]
        cn=request.form["contact"]

        con=sq.connect("student.db")
        cur=con.cursor()

        cur.execute("insert into student(name,email,password,contact) values(?,?,?,?)",[fn,em,ps,cn])

        con.commit()
        con.close()
    
        return render_template("formsave.html")
    else:
        return "something went wrong"

@app.route("/viewdata")
def viewdata():
    con=sq.connect("student.db")
    cur=con.cursor()
    data=cur.execute("select * from student order by id desc")
    con.commit()
    return render_template("viewdata.html",data=data)    


@app.route("/delete/<int:id>")
def delete(id):
     con=sq.connect("student.db")
     cur=con.cursor()
     cur.execute("delete  from student where id=?",[id])
     con.commit()
     return redirect("/viewdata")  

@app.route("/update/<int:id>") 
def update(id):
      con=sq.connect("student.db")
      cur=con.cursor()
      cur.execute("select * from student where id=?",[id])
      data=cur.fetchone()
      con.commit()
      return render_template("update.html",data=data) 

@app.route("/profilesave", methods=["GET","POST"])
def profilesave():
    if request.method=="POST":
        id=request.form["id"]
        n=request.form["name"]
        e=request.form["email"]
        p=request.form["password"]
        c=request.form["contact"]

        con=sq.connect("student.db")
        cur=con.cursor()
        cur.execute("update student set name=?,email=?,password=?,contact=? where id=?",[n,e,p,c,id])
        data=cur.fetchone()
        con.commit()
        return redirect(url_for("viewdata"))


@app.route("/loginview")
def login():
    return render_template("login.html")

@app.route("/logincheck",methods=["GET","POST"])
def logincheck():
    if request.method=="POST":
        em=request.form["email"]
        ps=request.form["password"]

        con=sq.connect("student.db")
        cur=con.cursor()
        cur.execute("select * from student where email=? and password=?",[em,ps])
        data=cur.fetchall()

        if data:
                session["username"]=em
                # return "Login Successful"
                return "<script>window.alert('Login successful');window.location.href='/dashboard';</script>"
        else:
            return "<script>window.alert('Login failed');window.location.href='/loginview';</script>"
    else:
        return "Error"


@app.route("/dashboard")    
def dashboard():
    if session.get("username") is not None: 
        un=session.get("username")
        con=sq.connect("student.db")
        cur=con.cursor()
        cur.execute("select * from student where email=?",[un])
        data=cur.fetchone()
        return render_template("dashboard.html",data=data)
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop('username',None)   # session end
    return redirect(url_for("login"))

@app.route("/file")
def file():
    return render_template("document_upload.html")

@app.route("/fileupload", methods=["GET","POST"])
def fileupload():
    if request.method=="POST":
        sn=request.files["myfile"]
        #sn.save(sn.filename)    # without folder path
        sn.save(os.path.join(app.config['upload_folder'],sn.filename))  # folder path
        return "uploaded successfully"
    else:
        return "failed"


if __name__=="__main__":
    app.run(debug=True)