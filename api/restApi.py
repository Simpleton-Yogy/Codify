from flask import Flask, request
from datetime import datetime
import json
import os
import re
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import bindparam

app = Flask(__name__, static_folder = './build', static_url_path = '/')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///storage/database.db"
db = SQLAlchemy(app)

class Profile(db.Model):
    name            = db.Column("First Name", db.String(255) ,primary_key = True)
    email           = db.Column("email", db.String(255),  unique = True)
    password        = db.Column("password", db.String(255))
    bioText         = db.Column("bioText", db.Text())
    bioTitle        = db.Column("bioTitle", db.String(255))
    characteristics = db.Column("characteristics", db.JSON)
    primarySkills   = db.Column("primarySkills", db.JSON)
    secondarySkills = db.Column("secondarySkills", db.JSON)
    careers         = db.Column("careers", db.JSON)

class Post(db.Model):
    title = db.Column("title", db.String(255), primary_key = True)
    text  = db.Column("text", db.Text())
    author = db.Column("author", db.String(255))
    time = db.Column("time", db.DateTime, default = datetime.now)

@app.route('/', methods = ["GET"])
def index():
    return app.send_static_file('index.html')

@app.route('/SignUp', methods = ["GET"])
def SignUp():
    return app.send_static_file('index.html')

@app.route('/find', methods = ["GET"])
def find():
    return app.send_static_file('index.html')

@app.route('/profile/<string:user>', methods = ["GET"])
def profile(user):
    return app.send_static_file('index.html')

@app.route('/SignUp', methods = ["POST"])
def getDataSignUp():
    data = request.json
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if data["name"] != "":

        if re.search(regex, data["mail"]):

            if data["bioText"] != "" and data["bioTitle"] != "":

                for i in data["characteristics"]:
                    if data["characteristics"][i] == "":
                        return("Invalid Characteristic Point")

                for i in data["primarySkills"]:
                    if data["primarySkills"][i] == "":
                        return("Invalid Primary Skill Point")

                for i in data["secondarySkills"]:
                    if data["secondarySkills"][i] == "":
                        return("Invalid Secondary Skill Point")

                for i in data["careers"]:
                    for o in data["careers"][i]:
                        if data["careers"][i][o] == "":
                            return("Invalid Career or School Info") 

                newUser = Profile(name = data["name"], 
                                email = data["mail"], 
                                password = data["password"], 
                                bioText = data["bioText"], 
                                bioTitle = data["bioTitle"], 
                                characteristics = data["characteristics"], 
                                primarySkills = data["primarySkills"],
                                secondarySkills = data["secondarySkills"],
                                careers = data["careers"])

                db.session.add(newUser)
                db.session.commit()
                return("success")

            else: 
                return("Invalid Bio Info")

        else: 
            return("Invalid Email")

    else: 
        return("Invalid Username")

@app.route('/profile/post', methods = ["POST"])
def sendProfile():
    data = request.json

    queryOutput = Profile.query.filter_by(name = data["name"]).first()
    output = {'name': queryOutput.name, 'bioText': queryOutput.bioText, 'bioTitle': queryOutput.bioTitle, 'characteristics': queryOutput.characteristics, 'primarySkills': queryOutput.primarySkills, 'secondarySkills': queryOutput.secondarySkills, 'careers': queryOutput.careers}
    outputFinal = json.dumps(output)

    return(outputFinal)

@app.route('/search', methods = ["POST"])
def handleSearch():
    data = request.json

    queryOutput = Profile.query.filter(Profile.name.contains(data["name"])).all()
    output = {}

    for i in range(len(queryOutput)):
        output["person_" + str(i)] = {'name': queryOutput[i].name, "characteristics": queryOutput[i].characteristics, "primarySkills": queryOutput[i].primarySkills}

    outputFinal = json.dumps(output)
    return(outputFinal)

@app.route('/logIn', methods = ["POST"])
def handleLogIn():
    data = request.json

    queryOutput = Profile.query.filter_by(name = data["name"]).first()

    if queryOutput == None:
        return("User does not exist")

    elif data["password"] == queryOutput.password:
        return("success")

    else: 
        return("Wrong Password")

@app.route('/post', methods = ["POST"])
def handlePost():
    data = request.json

    newPost = Post(title = data["title"],
                   text = data["text"],
                   author = data["author"])

    db.session.add(newPost)
    db.session.commit()

    return("success")

@app.route('/getAllPosts', methods = ["POST"])
def returnAllPosts():
    data = request.json
    output = {}

    formatString = "%H:%M %d %m %Y"

    queryOutput = Post.query.all()

    for i in range(len(queryOutput)):
        output["post_" + str(i)] = {'title': queryOutput[i].title, 'text': queryOutput[i].text, 'author': queryOutput[i].author, 'time': str(str(queryOutput[i].time.hour) + ":" + 
                                                                                                                                             str(queryOutput[i].time.minute) + "  " + 
                                                                                                                                             str(queryOutput[i].time.day) + ". " + 
                                                                                                                                             str(queryOutput[i].time.month) + ". " + 
                                                                                                                                             str(queryOutput[i].time.year))}

    outputFinal = json.dumps(output)

    return(output)

if __name__ == "__main__":
    app.run(host = "0.0.0.0", 
            port = os.environ.get('PORT', 40))
