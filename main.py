from flask import Flask, jsonify, request
import os
import sys
import subprocess
from backend import *

app = Flask(__name__)
my_backend = backend()

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

@app.route("/signup", methods=["POST"])
def createAccount():
    token = ""
    if request!=None:
        conta = request.json
        statusCode, token = my_backend.createNewUser({"email":conta["email"], "pwd":conta["pwd"]})
    return {"token":token}

@app.route("/login", methods=["POST"])
def login():
    conta = request.json
    statusCode, result = my_backend.login({"id":conta["id"], "pwd": conta["pwd"]})    
    return {"token":result}

@app.route("/updateAccount", methods=["PUT"])
def updateAccount():
    conta = request.json
    statusCode = my_backend.updateAccount(conta["token"],{"name":conta["name"], "dob":conta["dob"], "contact":conta["contact"], "academicDegree":conta["academicDegree"], "academicArea":conta["academicArea"], "bio":conta["bio"]})
    return f"{statusCode}"

@app.route("/updatePreferences", methods=["PUT"])
def updatePreferences():
    conta = request.json
    result = my_backend.updatePreferences(conta["token"], {"bph":conta["bph"], "studylocal":conta["studyLocal"], "music":conta["music"], "schedule":conta["schedule"], "talkative":conta["talkative"]})
    return f"{result}"

@app.route("/updateInterest", methods=["PUT"])
def updateInterests():
    conta = request.json
    result = my_backend.updateInterests(conta["token"], conta["interests"])
    return f"{result}"

@app.route("/getUserInterests", methods=["GET"])
def getUserInterests():
    conta = request.json
    result = my_backend.getUserInterests(conta["token"])
    return {"interests":result}

@app.route("/getProfileInfo", methods=["GET"])
def getProfileInfo():
    conta = request.json
    return {"pfp": "", "name": my_backend.getName(conta["token"]), "email":my_backend.getEmail(conta["token"]), "contact":my_backend.getContact(conta["token"]), "academicDegree": my_backend.getAcademicDegree(conta["token"]), "interests":my_backend.getUserInterests(conta["token"])}

@app.route("/getSuggestions", methods=["GET"])
def getSuggestions():
    conta = request.json
    result = my_backend.getSugestions(conta["token"])
    return result

@app.route("/getAllUsers", methods=["GET"])
def getAllUsers():
    return my_backend.getAllUsers()

@app.route("/swipe", methods=["POST"])
def swipe():
    conta = request.json
    token = conta["token"]
    targetid = conta["targetid"]
    swipeLeft = conta["left"]
    swipeRight = conta["right"]
    return my_backend.updateSwipe(token, {"userId":targetid, "left":swipeLeft, "right":swipeRight})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
