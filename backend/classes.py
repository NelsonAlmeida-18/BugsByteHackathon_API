from pydantic import BaseModel


class SignUp(BaseModel):
    email : str
    pwd : str
class Preferences(BaseModel):
    ageLowerBound : int
    ageUpperBound: int
    interests: int
    distance : int
    academics : int

class UpdateAccount(BaseModel):
    name : str
    dob : str
    contact : str
    academicDegree : str
    academicArea : str

class Preferences(BaseModel):
    bph : int
    studyLocal : str
    music : int
    schedule : int
    talkative : int

class Interests(BaseModel):
    interests : str

class Login(BaseModel):
    id:str
    pwd:str