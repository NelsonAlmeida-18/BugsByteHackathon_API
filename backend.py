import sqlite3
import jwt
from database_creator import *
from datetime import datetime, timedelta
import time
import os
import re

class backend:
    def __init__(self):
        connected = False
        iterations = 0
        #number of iterations hits 100 then it stops tryong to connect since some other
        #error might be impeding to connect
        while(not connected and iterations<100):
            #if db exists connect to it
            try:

                connection = sqlite3.connect('SmartMatch')

                cursor = connection.cursor()
                cursor.execute("SELECT * FROM user")
                result = cursor.fetchall()

                connected=True
                #jwt
                key = os.urandom(32)
                self.key = key

                print("Connected")
            #else create db then connect to it
            except:
                create_db()
                print(f"Retrying {iterations}")

            iterations+=1

        self.connection = connection

    def createJWT(self, userId):
        date_time = datetime.now()
        date_time = date_time + timedelta(minutes=30)
        
        encoded = jwt.encode({
            "userId": userId,
            "exp": time.mktime(date_time.timetuple())
        }, key=self.key)
        
        return encoded
    
    def decodeJWT(self, encoded):
        return jwt.decode(encoded, self.key, algorithms=["HS256"])
    
    def verifyExp(self, encoded):
        decode = self.decodeJWT(encoded)
        exp = decode["exp"]
        date = datetime.fromtimestamp(exp)
        if datetime.now() >= date:
            return False
        else:
            return True

    def convertToBinaryData(self, filename):
        # Convert digital data to binary format
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData
    
    def updateLocation(self, newLocation, id):
        cursor = self.connection.cursor()
        cursor.execute(f"UPDATE user SET location = '{newLocation}' WHERE id = '{id}'")

    def getInterestsColumns(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM interests")
        columns = list(map(lambda x: x[0], cursor.description))
        
        return columns


    def fillInterests(self, interests):
        allInterests = self.getInterestsColumns()
        cursor = self.connection.cursor()

        sqlite3_insert_interests = "INSERT INTO interests ("
        for i in range(1, len(allInterests)):
            sqlite3_insert_interests += allInterests[i]
            if i < len(allInterests)-1:
                sqlite3_insert_interests += ", "
            else:
                sqlite3_insert_interests += ") "

        sqlite3_insert_interests += "VALUES ("

        for i in range(1, len(allInterests)):
            if allInterests[i] in interests:
                sqlite3_insert_interests += "1"
            else:
                sqlite3_insert_interests += "0"

            if i < len(allInterests)-1:
                sqlite3_insert_interests += ", "
            else:
                sqlite3_insert_interests += ")"

        cursor.execute(sqlite3_insert_interests)

        cursor.execute("SELECT id FROM interests")
        result = cursor.fetchone()[0]
        return result
    
    def getInterestsByUserId(self, userid):
        query = f"SELECT * FROM interests where id = '{userid}'"
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        interests = self.getInterestsColumns()[1:]
        userInterests = []
        for i in range(len(result)):
            if result[i]==1:
                userInterests.append(interests[i])
        return userInterests
    

    def getSugestions(self, token):
        json = {}
        json["users"] = []
        suges = self.checkSimilarPreferences(token)
        for i in suges:
            dic = {}
            dic["userId"] = i[0]
            dic["name"] = i[1] 
            dic["pfp"] = i[2]
            dic["interests"] = self.getInterestsByUserId(i[0])
            json["users"].append(dic)

        return json
    
    def getUserInterests(self, token):
        valid = self.verifyExp(token)
        if valid:
            userId = self.decodeJWT(token)["userId"]
            query = f"SELECT * FROM interests where id = '{userId}'"
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            interests = self.getInterestsColumns()[1:]
            userInterests = []
            for i in range(len(result)):
                if result[i]==1:
                    userInterests.append(interests[i])
            return userInterests
        return []
    
    def getName(self, token):
        valid = self.verifyExp(token)
        if valid:
            userId = self.decodeJWT(token)["userId"]
            query = f"""SELECT name FROM user where id = '{userId}' """
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchone()[0]
            return result

        return ""
    
    def getEmail(self, token):
        valid = self.verifyExp(token)
        if valid:
            userId = self.decodeJWT(token)["userId"]
            query = f"""SELECT email FROM user where id = '{userId}' """
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchone()[0]
            return result

        return ""
    
    def getContact(self, token):
        valid = self.verifyExp(token)
        if valid:
            userId = self.decodeJWT(token)["userId"]
            query = f"""SELECT contact FROM user where id = '{userId}' """
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchone()[0]
            return result

        return ""
    
    def getAcademicDegree(self, token):
        valid = self.verifyExp(token)
        if valid:
            userId = self.decodeJWT(token)["userId"]
            query = f"""SELECT academicDegree FROM user where id = '{userId}' """
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchone()[0]
            return result

        return ""

    def getInterestsColumns(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM interests")
        columns = list(map(lambda x: x[0], cursor.description))
        
        return columns

    def getInterests(self):
        return {"interests":self.getInterestsColumns()[1:]}
    
    def postInterests(self, token, payload):
        valid = self.verifyExp(token)
        if valid:
            cursor = self.connection.cursor()
            userId = self.decodeJWT(token)["userId"]
            queries = []
            for interest in payload["interests"]:
                queries.append(f"""UPDATE INTEREST SET {interest}=1 WHERE id='{userId}'""")

        
        return 420, None

    def initializePreferences(self):
        cursor = self.connection.cursor()
        cursor.execute(f'''INSERT INTO preferences 
                        (bph, studylocal, music, schedule, talkative) VALUES 
                        ('0', '', '0', '0', '0')''')
        cursor.execute("SELECT MAX(id) FROM preferences")
        id = cursor.fetchone()[0]
        return id
    
    def updatePreferences(self, token, payload):
        valid = self.verifyExp(token)
        if valid:
            userId = self.decodeJWT(token)["userId"]
            cursor = self.connection.cursor()
            cursor.execute(f'''UPDATE preferences SET 
                            bph = "{payload["bph"]}",
                            studylocal = "{payload["studylocal"]}",
                            music = "{payload["music"]}",
                            schedule = "{payload["schedule"]}",
                            talkative = "{payload["talkative"]}"
                            WHERE id = "{userId}" ''')
            return 200
        return 420
    
    def updateInterests(self, token, payload):
        valid = self.verifyExp(token)
        if valid:
            allInterests = self.getInterestsColumns()
            cursor = self.connection.cursor()

            #é o mesmo id do que o userId
            #cursor.execute(f"SELECT user_interests FROM user WHERE id = '{id}';")
            #user_interests = cursor.fetchone()[0]

            sqlite3_update = "UPDATE interests SET "

            for i in range(0, len(allInterests)):
                if allInterests[i] in payload:
                    sqlite3_update += allInterests[i] + " = 1"
                else:
                    sqlite3_update += allInterests[i] + " = 0"
                
                if i < len(allInterests)-1:
                    sqlite3_update += ", "
            userId = self.decodeJWT(token)["userId"]
            sqlite3_update += f" WHERE id = '{userId}';"

            cursor.execute(sqlite3_update)

            return 200
        return 420
    

    def newMatch(self, fromid, toid):
        cursor = self.connection.cursor()
        cursor.execute(f'INSERT INTO match (fromid, toid) VALUES ("{fromid}", "{toid}")')
        return 200
    

    def updateSwipe(self, token, payload):
        valid = self.verifyExp(token)
        if valid:
            userid = self.decodeJWT(token)["userId"]
            cursor = self.connection.cursor()
            cursor.execute(f'''INSERT INTO swipe
                            (userid, targetid, right, left) VALUES 
                            ("{userid}", "{payload["targetId"]}", "{payload["right"]}", "{payload["left"]}")''')

            cursor.execute(f'SELECT right FROM swipe WHERE userid = "{payload["targetid"]}" AND targetid = "{userid}"')
            result = cursor.fetchone()[0]
            if result == 1:
                self.newMatch(userid, payload["targetId"])
                self.newMatch(payload["targetId"], userid)
            return 200
        
        return 420
    

    def addPlace(self, token, payload):
        valid = self.verifyExp(token)
        if valid:
            userid = self.decodeJWT(token)["userId"]
            cursor = self.connection.cursor()
            cursor.execute(f'''INSERT INTO place (street, city, country, studytype, rating) 
                            VALUES ("{payload["street"]}", "{payload["city"]}", "{payload["country"]}", "{payload["studytype"]}", "{payload["rating"]}")''')
            
            return 200

        return 420


    def createNewUser(self, payload):
        pwd = payload["pwd"]
        email = payload["email"]
        username = ""
        dob = ""
        bio = ""
        academicArea = ""
        academicDegree = ""
        picture = ""
        location = ""
        

        cursor = self.connection.cursor()
        # check if user exists in db
        sqlite_checkUser_query = f"""SELECT COUNT(*) FROM user where
                                    email = '{email}'"""
        cursor.execute(sqlite_checkUser_query)
        result = cursor.fetchone()[0]
        #user already exists
        if result!=0:
            return 420, None

        #add interests
        user_interests = self.fillInterests([])

        #add preferences
        preferences = self.initializePreferences()

        #create user
        sqlite_createNewUser_query = f"""INSERT INTO user
                                       (name,email,pwd,dob,academicArea,academicDegree, picture, user_interests, location, user_preferences)
                                        values ('{username}', '{email}', '{pwd}', '{dob}', 
                                                '{academicArea}', '{academicDegree}', 
                                                '{picture}', '{preferences}', '{location}', '{preferences}')
                                    """

        cursor.execute(sqlite_createNewUser_query)
        cursor.execute('''
                    SELECT max(id) FROM user''')
        userid = cursor.fetchone()[0]
        return 200,self.createJWT(int(userid))

    def updateAccount(self, token, payload):
        valid = self.verifyExp(token)
        if valid:
            userId = self.decodeJWT(token)["userId"]

            name = payload["name"]
            dob = payload["dob"]
            contact = payload["contact"]
            academicDegree = payload["academicDegree"]
            academicArea = payload["academicArea"]
            bio = payload["bio"]

            query = f"""UPDATE user SET name = '{name}', dob = '{dob}', contact = '{contact}' , academicDegree =' {academicDegree}', academicArea = '{academicArea}', bio = '{bio}'
                    WHERE id = '{userId}';
            """

            cursor = self.connection.cursor()
            cursor.execute(query)
            return 200
        #invalid token
        return 420



    def login(self, payload):
        id = payload["id"]
        pwd = payload["pwd"]
  
        sqlite_checkUser_query = f""" SELECT id from user
                                        WHERE email = '{id}' AND pwd = '{pwd}' 
                                """
            
        cursor = self.connection.cursor()

        cursor.execute(sqlite_checkUser_query)
        result = cursor.fetchone()
    
        if result != None:
            return 200,self.createJWT(int(result[0]))
        else:
            return 420, None
        
    def getAllUsers(self):
        sqlite_getUsers_query = """SELECT * FROM user"""        
        cursor = self.connection.cursor()
        cursor.execute(sqlite_getUsers_query)
        return cursor.fetchall()
    
    def checkSimilarPreferences(self, token):
        valid = self.verifyExp(token)
        if valid:
            userid = self.decodeJWT(token)["userId"]
            cursor = self.connection.cursor()
            cursor.execute(f'''SELECT u.id, u.name, u.email, u.location,
                            COUNT(*) AS num_common_interests,
                            SUM(CASE WHEN p.bph = my_pref.bph THEN 1 ELSE 0 END) AS bph_match,
                            SUM(CASE WHEN p.studylocal = my_pref.studylocal THEN 1 ELSE 0 END) AS studylocal_match,
                            SUM(CASE WHEN p.music = my_pref.music THEN 1 ELSE 0 END) AS music_match,
                            SUM(CASE WHEN p.schedule = my_pref.schedule THEN 1 ELSE 0 END) AS schedule_match,
                            SUM(CASE WHEN p.talkative = my_pref.talkative THEN 1 ELSE 0 END) AS talkative_match
                            FROM user u
                            JOIN interests i ON u.user_interests = i.id
                            JOIN preferences p ON u.user_preferences = p.id
                            JOIN user my_user ON my_user.id = "{userid}"
                            JOIN interests my_int ON my_user.user_interests = my_int.id
                            JOIN preferences my_pref ON my_user.user_preferences = my_pref.id
                            LEFT JOIN swipe s ON u.id = s.targetid AND s.userid = my_user.id
                            WHERE u.id <> my_user.id AND s.right IS NULL AND s.left IS NULL
                            AND (i.Mathematics = my_int.Mathematics OR i.Portuguese = my_int.Portuguese OR i.English = my_int.English
                            OR i.German = my_int.German OR i.Physics = my_int.Physics OR i.Chemistry = my_int.Chemistry
                            OR i.Economics = my_int.Economics OR i.Biology = my_int.Biology OR i.Geology = my_int.Geology
                            OR i.History = my_int.History OR i.Computing = my_int.Computing OR i.Engineering = my_int.Engineering
                            OR i.Medicine = my_int.Medicine OR i.Nursing = my_int.Nursing OR i.Pharmacy = my_int.Pharmacy
                            OR i.Education = my_int.Education OR i.Law = my_int.Law OR i.Psychology = my_int.Psychology
                            OR i.Politics = my_int.Politics OR i.Sports = my_int.Sports
                            OR p.bph = my_pref.bph OR p.studylocal = my_pref.studylocal OR p.music = my_pref.music
                            OR p.schedule = my_pref.schedule OR p.talkative = my_pref.talkative)
                            GROUP BY u.id
                            ORDER BY num_common_interests DESC;''')

            result = cursor.fetchall()
            return result
        return []
    
    def getUserMatches(self, token):
        valid = self.verifyExp(token)
        if valid:
            cursor = self.connection.cursor()
            userid = self.decodeJWT(token)
            cursor.execute("SELECT toid FROM match WHERE fromid = '{userid}'")
            
            result = cursor.fetchall()
            return result
        
        return 420

    def getUsers(self, token, preferences):
        #decrypt token
        valid = self.verifyExp(token)

        if valid:
            queries= [f"""SELECT id FROM user WHERE julianday('now') - julianday(user.dob) >= {preferences[preference]} AND
                                                            julianday('now') - julianday(user.dob) <= {preferences[preference]}"""]
    
            if preferences["interests"]==1:
                query = """SELECT u.id
                            FROM user u
                            INNER JOIN interests i ON u.interests_id = i.id
                            WHERE i.Mathematics = {current_user.Mathematics}
                            AND i.Portuguese = {current_user.Portuguese}
                            AND i.English = {current_user.English}
                            AND i.German = {current_user.German}
                            AND i.Physics = {current_user.Physics}
                            AND i.Chemistry = {current_user.Chemistry}
                            AND i.Economics = {current_user.Economics}
                            AND i.Biology = {current_user.Biology}
                            AND i.Geology = {current_user.Geology}
                            AND i.History = {current_user.History}
                            AND i.Computing = {current_user.Computing}
                            AND i.Engineering = {current_user.Engineering}
                            AND i.Medicine = {current_user.Medicine}
                            AND i.Nursing = {current_user.Nursing}
                            AND i.Pharmacy = {current_user.Pharmacy}
                            AND i.Education = {current_user.Education}
                            AND i.Law = {current_user.Law}
                            AND i.Psychology = {current_user.Psychology}
                            AND i.Politics = {current_user.Politics}
                            AND i.Sports = {current_user.Sports}
                            AND u.id != {current_user.id};
                        """
                queries.append(query)
                
            

        #expired token
        return 424, None

