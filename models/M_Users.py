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

    def GetUserData(self, id):
        mycursor = self.connDB.cursor()
        mycursor.execute("SELECT * FROM Users WHERE `id` = '"+str(id)+"'")
        return mycursor.fetchall()
        

    def LoginByUsername(self, username, password):
        mycursor = self.connDB.cursor()
        mycursor.execute("SELECT * FROM Users WHERE `username` = '"+username+"'")
        res = mycursor.fetchall()
        if len(res): 
            _id = res[0][0]
            _password = res[0][7]
            passHash = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if passHash == _password.lower():
                tok = self.GenerateUserToken(_id)
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
            _id, _username, _email, _fstname, _lstname, _birthday, _creationDate, _password = res[0]
            passHash = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if passHash == _password.lower():
                tok = self.GenerateUserToken(_id)
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

    def GenerateUserToken(self, id):
        ts = int(time.time() * 1000)
        #ex = ts +  1000 * 3600 * 24 * 365 # expire in one year : time is in milliseconds
        ex = ts + 1000 * 3600 * 24 * 7 # expire in one week : time is in milliseconds
        tsHash = hashlib.sha256(str(ex).encode('utf-8')).hexdigest()
        core = {
            "timestamp": ts,
            "expiration": ex,
            "id": id,
            "hash": tsHash
        }
        parsedCore = json.dumps(core)
        return config.Cryptography.Encode64(parsedCore)    

    def SetUserEmailStatus(self, id, state): # index 0
        mycursor = self.connDB.cursor()
        mycursor.execute("SELECT * FROM Users WHERE `id` = '"+str(id)+"'")
        res = mycursor.fetchall()
        if len(res): 
            userId = id
            _status = res[0][9]
            if state:
                _status = _status | 0b00000001
            else:
                _status = _status & 0b11111110
            sql = (""  
                "UPDATE `Users` SET `status` = '"+str(_status)+"' WHERE `Users`.`id` = "+str(userId)+";"
            "")
            mycursor.execute(sql)
            self.connDB.commit()
            return {
                    "success": True
                }
        return {
            "success": False,
            "message": "Error while setting user status"
        }
    
    def SetUserPhoneStatus(self, id, state): # index 1
        mycursor = self.connDB.cursor()
        mycursor.execute("SELECT * FROM Users WHERE `id` = '"+str(id)+"'")
        res = mycursor.fetchall()
        if len(res): 
            userId = id
            _status = res[0][9]
            if state:
                _status = _status | 0b00000010
            else:
                _status = _status & 0b11111101
            sql = (""  
                "UPDATE `Users` SET `status` = '"+str(_status)+"' WHERE `Users`.`id` = "+str(userId)+";"
            "")
            mycursor.execute(sql)
            self.connDB.commit()
            return {
                    "success": True
                }
        return {
            "success": False,
            "message": "Error while setting user status"
        }

    def SetUserBannedStatus(self, id, state): # index 2
        mycursor = self.connDB.cursor()
        mycursor.execute("SELECT * FROM Users WHERE `id` = '"+str(id)+"'")
        res = mycursor.fetchall()
        if len(res): 
            userId = id
            _status = res[0][9]
            if state:
                _status = _status | 0b00000100
            else:
                _status = _status & 0b11111011
            sql = (""  
                "UPDATE `Users` SET `status` = '"+str(_status)+"' WHERE `Users`.`id` = "+str(userId)+";"
            "")
            mycursor.execute(sql)
            self.connDB.commit()
            return {
                    "success": True
                }
        return {
            "success": False,
            "message": "Error while setting user status"
        }

    def SendConfirmationCode(self, id, mode): # mode 1: email; mode 2: phone
        mycursor = self.connDB.cursor()
        ts = int(time.time() * 1000)
        code = config.random.randint(100000, 999999)
        mycursor.execute("SELECT * FROM Users WHERE `id` = '"+str(id)+"'")
        res = mycursor.fetchall()
        if len(res): 
            userId = id
            _phone = res[0][8]
            _email = res[0][2]
        sql = (""  
                "INSERT INTO `Confirmation` (`id`, `user_id`, `confirmation_code`, `timestamp`) "
                "VALUES (NULL, '"+str(userId)+"', '"+str(code)+"', '"+str(ts)+"');"
            "")
        mycursor.execute(sql)
        self.connDB.commit()
        if mode==1:
            pass # send code by email
        elif mode==2:
            pass # send code by phone sms
        return {
                "success": True
            }


