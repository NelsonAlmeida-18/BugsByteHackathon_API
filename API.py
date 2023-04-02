from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import subprocess
from classes import *
from backend import *
import datetime
import json

app = FastAPI()
my_backend = backend()

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'fastapi[all]']

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/signup")
async def createAccount(conta:SignUp):
    if conta!=None:
        statusCode, payload = my_backend.createNewUser({"email":conta.email, "pwd":conta.pwd})
        if statusCode!=200:
            raise HTTPException(status_code = 422, detail="User already exists")
        return payload

@app.post("/login")
async def login(user:Login):
    statusCode, result = my_backend.login({"id":user.id, "pwd": user.pwd})

    if statusCode!=200:
        raise HTTPException(status_code=422, detail="Invalid username or password")
    
    return result

@app.put("/updateAccount")
async def updateAccount(account:UpdateAccount, token:str):
    statusCode = my_backend.updateAccount(token,{"name":account.name, "dob":account.dob, "contact":account.contact, "academicDegree":account.academicDegree, "academicArea":account.academicArea})
    if statusCode!=200:
        raise HTTPException(status_code=420, detail="Invalid token")
    return 200

@app.put("/updatePreferences")
async def updatePreferences(token:str, payload:Preferences):
    result = my_backend.updatePreferences(token, {"bph":payload.bph, "studylocal":payload.studyLocal, "music":payload.music, "schedule":payload.schedule, "talkative":payload.talkative})
    if result!=200:
        raise HTTPException(status_code=420, detail="Invalid token")

@app.put("/updateInterest")
async def updateInterests(token:str, payload:str):
    result = my_backend.updateInterest(token, payload.split(","))
    if result!=200:
        raise HTTPException(status_code=420, detail="Invalid token")

@app.get("/getAllUsers")
async def getAllUsers():
    return my_backend.getAllUsers()

@app.get("/getInterests")
async def getInterests():
    return my_backend.getInterests()

@app.post("/swipeRight")
async def swipeRight(token:str, targetId:str):
    #result = my_backend.swipeRight(token, targetId)
    result=200
    if result!=200:
        raise HTTPException(status_code=420, detail="Invalid token")
    
@app.get("/getUsersWithSimilar")
async def getUsersWithSimilar(token):
    result = my_backend.checkSimilarPreferences(token)
    print(result)
    return 200

@app.get("/getMatches")
async def getMatches(token:str):
    return 200
