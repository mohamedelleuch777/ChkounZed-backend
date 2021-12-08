import config
import mysql.connector
import jwt
import time
import sys
import hashlib
import json

class M_Users : 
    connDB = None
    def __init__ (self):
        self.connDB = mysql.connector.connect(
            host="remotemysql.com",
            user="O4pKtnrYIk",
            password="hd0iDziUDK",
            database="O4pKtnrYIk"
        )

    def ListAllUsers(self):
        mycursor = self.connDB.cursor()
        mycursor.execute("SELECT * FROM Users")
        return mycursor.fetchall()

    def GetUserByEmail(self, email):
        mycursor = self.connDB.cursor()
        mycursor.execute("SELECT * FROM Users WHERE `email` = '"+email+"'")
        return mycursor.fetchall()

    def GetUserData(self, bearerTok):
        email = self.GetDataFromToken(bearerTok,'email')
        mycursor = self.connDB.cursor()
        mycursor.execute("SELECT * FROM Users WHERE `email` = '"+email+"'")
        res = mycursor.fetchall()
        if len(res): 
            we, _username, _email, _fstname, _lstname, _birthday, _creationDate, _password = res[0]
            return {
                    "success": True,
                    "id": we,
                    "username": _username,
                    "email": _email,
                    "firstname": _fstname,
                    "lastname": _lstname,
                    "birthday": _birthday,
                    "creation_date": _creationDate
                }
        return {
            "success": False,
            "message": "Error while reading user data"
        }

    def LoginByUsername(self, username, password):
        mycursor = self.connDB.cursor()
        mycursor.execute("SELECT * FROM Users WHERE `username` = '"+username+"'")
        res = mycursor.fetchall()
        if len(res): 
            we, _username, _email, _fstname, _lstname, _birthday, _creationDate, _password = res[0]
            passHash = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if passHash == _password.lower():
                tok = self.GenerateUserToken(_email)
                return {
                    "success": True,
                    "message": "Logged In",
                    "token": tok 
                }
            return {
                "success": False,
                "message": "Not logged In"
            }
            # if passHash == _password.lower():
            #     return '{"success": true, "message": "logged in"}'
            # return '{"success": false, "message": "wrong username/password"}'

    def LoginByEmail(self, email, password):
        mycursor = self.connDB.cursor()
        mycursor.execute("SELECT * FROM Users WHERE `email` = '"+email+"'")
        res = mycursor.fetchall()
        if len(res): 
            we, _username, _email, _fstname, _lstname, _birthday, _creationDate, _password = res[0]
            passHash = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if passHash == _password.lower():
                tok = self.GenerateUserToken(_email)
                return {
                    "success": True,
                    "message": "Logged In",
                    "token": tok 
                }
            return {
                "success": False,
                "message": "Not logged In"
            }

    def GenerateUserToken(self, email):
        ts = int(time.time() * 1000)
        ex = ts + 3600 * 24 * 365 # expire in one year
        tsHash = hashlib.sha256(str(ex).encode('utf-8')).hexdigest()
        core = {
            "timestamp": ts,
            "expiration": ex,
            "email": email,
            "hash": tsHash
        }
        parsedCore = json.dumps(core)
        return config.Cryptography.Encode64(parsedCore)

    def GetDataFromToken(self, token, key):
        decodedToken = config.Cryptography.Decode64(token.split(' ')[1])
        json_object = json.loads(decodedToken)
        return json_object[key]

    # Function to convert  
    def listToString(self,s): 
        
        # initialize an empty string
        str1 = "" 
            
        # traverse in the string  
        for ele in s: 
            str1 += str(ele)  

        # return string  
        return str1 