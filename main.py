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
    if request!=None:
        conta = request.json
        statusCode, payload = my_backend.createNewUser({"email":conta["email"], "pwd":conta["pwd"]})
        if statusCode!=200:
            return ""
        return payload
    return ""

@app.route("/login", methods=["POST"])
def login():
    conta = request.json
    statusCode, result = my_backend.login({"id":conta["id"], "pwd": conta["pwd"]})
    if statusCode!=200:
        return ""    
    return result

@app.route("/updateAccount", methods=["PUT"])
def updateAccount():
    conta = request.json
    statusCode = my_backend.updateAccount(conta["token"],{"name":conta["name"], "dob":conta["dob"], "contact":conta["contact"], "academicDegree":conta["academicDegree"], "academicArea":conta["academicArea"]})
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

@app.route("/getInterests", methods=["GET"])
def getInterests():
    return {"interests" : my_backend.getInterests()}


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
