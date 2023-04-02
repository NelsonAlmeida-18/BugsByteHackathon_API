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
async def login():
    request = request.json
    statusCode, result = my_backend.login({"id":request["id"], "pwd": request["pwd"]})
    if statusCode!=200:
        return ""    
    return result



if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
