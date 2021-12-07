import config
import mysql.connector
import jwt
import datetime
import sys
import hashlib

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

    def LoginByUsername(self, username, password):
        mycursor = self.connDB.cursor()
        mycursor.execute("SELECT * FROM Users WHERE `username` = '"+username+"'")
        res = mycursor.fetchall()
        if len(res): 
            we, _username, _email, _fstname, _lstname, _birthday, _creationDate, _password = res[0]
            passHash = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if passHash == _password.lower():
                tok = self.GenerateUserToken()
                return '''
                {
                    "success": true,
                    "message": "Logged In",
                    "token": "'''+ tok + '''"
                }
                '''
            return '''
            {
                "success": false,
                "message": "Not logged In"
            }
            '''
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
                tok = self.GenerateUserToken()
                return '''
                {
                    "success": true,
                    "message": "Logged In",
                    "token": "'''+ tok + '''"
                }
                '''
            return '''
            {
                "success": false,
                "message": "Not logged In"
            }
            '''

    def GenerateUserToken(self):
        return "EFWfnew432GENf23FINEFI+FWNEISA"

    # Function to convert  
    def listToString(self,s): 
        
        # initialize an empty string
        str1 = "" 
            
        # traverse in the string  
        for ele in s: 
            str1 += str(ele)  

        # return string  
        return str1 