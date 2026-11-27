import sqlite3 as sq
con=sq.connect("student.db")
cur=con.cursor()

# cur.execute("create table student(id INTEGER PRIMARY KEY AUTOINCREMENT,name varchar(50),email varchar(50),password int, contact int)")
cur.execute("insert into student (name,email,password,contact) values(?,?,?,?)",["shiv","shiv@gmail.com",123,987645])
# # cur.execute("delete from student where password=123")
# cur.execute("delete * from student")





con.commit()
con.close()