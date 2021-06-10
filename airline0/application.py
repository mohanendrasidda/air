import os
from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
app=Flask(__name__)
engine=create_engine("postgresql://postgres:mohan@localhost:5432/postgres")
db=scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    flights=db.execute("SELECT *FROM flights").fetchall()
    return render_template("index.html",flights=flights)

@app.route("/book", methods=["POST"])
def book():
    name=request.form.get("name")
    if not name:
        return render_template("error.html",message= "error: enter your name to book a flight")
    flight_id=request.form.get("flight_id")
    if not flight_id:
         return render_template("error.html",message= "error: select a flight to book")
    db.execute("INSERT INTO passengers(name,flight_id)  VALUES(:name,:flight_id)",{"name":name, "flight_id":flight_id})
    db.commit()
    return render_template("success.html")
