from flask import *
import sqlite3 as sq
app=Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/enquire")
def reg():
    return render_template("enquire.html")

@app.route("/savedata",methods=["GET","POST"])
def savedata():
    if request.method=="POST":
        name=request.form['name']
        email=request.form['email']
        contact=request.form['contact']
        messege=request.form['messege']

        con=sq.connect("fortune.db")
        cur=con.cursor()
        cur.execute("create table if not exists user(id INTEGER PRIMARY KEY AUTOINCREMENT, name varchar(100),email varchar(100), contact int ,messege varchar(400))")
        cur.execute("insert into user(name,email,contact,messege) values(?,?,?,?)",[name,email,contact,messege])
        con.commit()
        con.close()
        return "data inserted successfully"
    else:
        return "something went wrong"

@app.route("/View")    
def view():
    con=sq.connect("fortune.db")
    cur=con.cursor()
    data=cur.execute("select * from user")
    con.commit()
    return render_template("viewdata.html",data=data)

@app.route("/delete/<int:id>")
def delete(id):
    con=sq.connect("fortune.db")
    cur=con.cursor()
    cur.execute("delete from user where id=?",[id])
    con.commit()
    return redirect(url_for("view"))

@app.route("/update/<int:id>")
def update(id):
    con=sq.connect("fortune.db")
    cur=con.cursor()
    cur.execute("select * from user where id=?",[id])
    data=cur.fetchone()
    con.commit()
    return render_template("update.html",data=data)

@app.route("/profileupdate",methods=["GET","POST"])
def profileupdate():
    con=sq.connect("fortune.db")
    cur=con.cursor()
    if request.method=="POST":
        id=request.form["id"]
        name=request.form["name"]
        email=request.form["email"]
        contact=request.form["contact"]
        messege=request.form["messege"]
        cur.execute("update user set name=?,email=?,contact=?,messege=? where id=?",[name,email,contact,messege,id])
        con.commit()
        con.close()
        return redirect(url_for("view"))
    return "something went wrong"










if __name__=="__main__":
    app.run(debug=True)
