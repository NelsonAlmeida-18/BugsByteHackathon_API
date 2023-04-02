from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from classes import *
from backend import *
import datetime
import json

app = FastAPI()
my_backend = backend()

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

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
