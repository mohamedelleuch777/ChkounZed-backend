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
        if email!=None:
            return self.cM_Users.LoginByEmail(email,password)
        else:
            return self.cM_Users.LoginByUsername(username,password)
    
    def GetAllUsers(self):
        self.ForceMethod('GET')
        return self.cM_Users.ListAllUsers()
    
    def GetUser(self):
        self.ForceMethod('GET')
        bearerTok = self.GetBearerToken()
        return self.cM_Users.GetUserData(bearerTok)
        
    def CreateUser(self):
        # here
        self.ForceMethod('POST')
        args = self.GetPostArgs()
        return self.cM_Users.CreateUserCore(args)
        
    def ActivateEmail(self):
        self.ForceMethod('GET')
        bearerTok = self.GetBearerToken()
        return self.cM_Users.SetUserEmailStatus(bearerTok, True)
        
    def InactivateEmail(self):
        self.ForceMethod('GET')
        bearerTok = self.GetBearerToken()
        return self.cM_Users.SetUserEmailStatus(bearerTok, False)
        
    def ActivatePhone(self):
        self.ForceMethod('GET')
        bearerTok = self.GetBearerToken()
        return self.cM_Users.SetUserPhoneStatus(bearerTok, True)
        
    def InactivatePhone(self):
        self.ForceMethod('GET')
        bearerTok = self.GetBearerToken()
        return self.cM_Users.SetUserPhoneStatus(bearerTok, False)
        
    def Ban(self):
        self.ForceMethod('GET')
        bearerTok = self.GetBearerToken()
        return self.cM_Users.SetUserBannedStatus(bearerTok, True)
        
    def Unban(self):
        self.ForceMethod('GET')
        bearerTok = self.GetBearerToken()
        return self.cM_Users.SetUserBannedStatus(bearerTok, False)
        
    def SendConfirmationCodeEmail(self):
        self.ForceMethod('GET')
        bearerTok = self.GetBearerToken()
        return self.cM_Users.SendConfirmationCode(bearerTok, 1)
        
    def SendConfirmationCodePhone(self):
        self.ForceMethod('GET')
        bearerTok = self.GetBearerToken()
        return self.cM_Users.SendConfirmationCode(bearerTok, 2)
        