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
        self.CheckTokenValidity(bearerTok)
        email = self.GetDataFromToken(bearerTok,'email')
        mycursor = self.connDB.cursor()
        mycursor.execute("SELECT * FROM Users WHERE `email` = '"+email+"'")
        res = mycursor.fetchall()
        if len(res): 
            we, _username, _email, _fstname, _lstname, _birthday, _creationDate, _password, _phone, _status = res[0]
            return {
                    "success": True,
                    "id": we,
                    "username": _username,
                    "email": _email,
                    "firstname": _fstname,
                    "lastname": _lstname,
                    "birthday": _birthday,
                    "creation_date": _creationDate,
                    "phone": _phone,
                    "status": _status
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
            _email = res[0][2]
            _password = res[0][7]
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

    def CreateUserCore(self, args):
        mycursor = self.connDB.cursor()
        lastIdBeforeInsert = mycursor.lastrowid
        passHash = hashlib.sha256(args['password'].encode('utf-8')).hexdigest()
        passHash = passHash.upper()
        # ts stores the time in milliseconds
        ts = int(time.time() * 1000)
        core = {}
        try:
            sql = (""  
                "INSERT INTO `Users` (`id`, `username`, `email`, `firstname`, `lastname`, `birthday`, `creationDate`, `password`, `phone`, `status`)"
                "VALUES (NULL, '"+args['username']+"', '"+args['email']+"', '"+args['firstname']+"', '"+args['lastname']+"', '"+
                args['birthday']+"', '"+str(ts)+"', '"+passHash+"', '"+args['phone']+"', '0');"
            "")
            mycursor.execute(sql)
            self.connDB.commit()
            core = {
                "success": lastIdBeforeInsert != mycursor.lastrowid,
            }
            # if came here that means the record has been created then, we can get the new user id to create its wallet
            mycursor = self.connDB.cursor()
            mycursor.execute("SELECT * FROM Users WHERE `email` = '"+args['email']+"'")
            res = mycursor.fetchall()
            userId = res[0][0]
            sql = (""
                "INSERT INTO `Wallet` (`id`, `user_id`, `currency_name`, `currency_symbol`, `payment_processor_1_id`, `payment_processor_1_balance`)"
                "VALUES (NULL, '"+str(userId)+"', 'TRY', '₺', '', '0' );"
            "")
            mycursor.execute(sql)
            self.connDB.commit()
        except Exception as e:
            core = {
                "success": lastIdBeforeInsert != mycursor.lastrowid,
                "message": str(e)
            }
        parsedCore = json.dumps(core)
        return parsedCore

    def GenerateUserToken(self, email):
        ts = int(time.time() * 1000)
        #ex = ts +  1000 * 3600 * 24 * 365 # expire in one year : time is in milliseconds
        ex = ts + 1000 * 3600 * 24 * 7 # expire in one week : time is in milliseconds
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

    def CheckTokenValidity(self, token):
        expiration = self.GetDataFromToken(token,'expiration')
        ts = int(time.time() * 1000)
        if int(expiration) < int(ts):
            error = {
                "success": False,
                "message": 'The auth token was expired!'
            }
            parsedError = json.dumps(error)
            config.ThrowException('401'+parsedError)

    # Function to convert  
    def listToString(self,s): 
        
        # initialize an empty string
        str1 = "" 
            
        # traverse in the string  
        for ele in s: 
            str1 += str(ele)  

        # return string  
        return str1 