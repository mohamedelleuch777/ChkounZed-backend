import config

class Users( config.Controller ) :
    cM_Users = None
    def __init__ (self):
        self.cM_Users = config.importModule("models/M_Users").M_Users()
        
    
    
    def run(self):
        return config.REQUEST_ARGS

    def Login(self):
        self.ForceMethod('GET')
        email = self.GetParam('email')
        username = self.GetParam('username')
        password = self.GetParam('password')
        if email!=None and  password!=None:
            return self.cM_Users.LoginByEmail(email,password)
        elif username!=None and  password!=None:
            return self.cM_Users.LoginByUsername(username,password)
        else:
            config.ReturnJsonError("Missing parameter for the GET request")
    
    def GetAllUsers(self):
        self.ForceMethod('GET')
        return self.cM_Users.ListAllUsers()
    
    def GetUser(self):
        self.ForceMethod('GET')
        bearerTok = self.GetBearerToken()
        id = self.GetDataFromToken(bearerTok,'id')
        user_id = self.GetParam('userId')
        if user_id:
            id = user_id
        res = self.cM_Users.GetUserData(id)
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
        
    def CreateUser(self):
        # here
        self.ForceMethod('POST')
        args = self.GetPostArgs()
        return self.cM_Users.CreateUserCore(args)
        
    def ActivateEmail(self):
        self.ForceMethod('GET')
        bearerTok = self.GetBearerToken()
        id = self.GetDataFromToken(bearerTok,'id')
        return self.cM_Users.SetUserEmailStatus(id, True)
        
    def InactivateEmail(self):
        self.ForceMethod('GET')
        bearerTok = self.GetBearerToken()
        id = self.GetDataFromToken(bearerTok,'id')
        return self.cM_Users.SetUserEmailStatus(id, False)
        
    def ActivatePhone(self):
        self.ForceMethod('GET')
        bearerTok = self.GetBearerToken()
        id = self.GetDataFromToken(bearerTok,'id')
        return self.cM_Users.SetUserPhoneStatus(id, True)
        
    def InactivatePhone(self):
        self.ForceMethod('GET')
        bearerTok = self.GetBearerToken()
        id = self.GetDataFromToken(bearerTok,'id')
        return self.cM_Users.SetUserPhoneStatus(id, False)
        
    def Ban(self):
        self.ForceMethod('GET')
        bearerTok = self.GetBearerToken()
        id = self.GetDataFromToken(bearerTok,'id')
        return self.cM_Users.SetUserBannedStatus(id, True)
        
    def Unban(self):
        self.ForceMethod('GET')
        bearerTok = self.GetBearerToken()
        id = self.GetDataFromToken(bearerTok,'id')
        return self.cM_Users.SetUserBannedStatus(id, False)
        
    def SendConfirmationCodeEmail(self):
        self.ForceMethod('GET')
        bearerTok = self.GetBearerToken()
        id = self.GetDataFromToken(bearerTok,'id')
        return self.cM_Users.SendConfirmationCode(id, 1)
        
    def SendConfirmationCodePhone(self):
        self.ForceMethod('GET')
        bearerTok = self.GetBearerToken()
        id = self.GetDataFromToken(bearerTok,'id')
        return self.cM_Users.SendConfirmationCode(id, 2)
        