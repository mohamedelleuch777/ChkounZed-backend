import config
import sys

class Users( config.Controller ) :
    cM_Users = None
    def __init__ (self):
        self.cM_Users = config.importModule("models/M_Users").M_Users()
        
    
    
    def run(self):
        return config.REQUEST_ARGS
    
    def GetAllUsers(self):
        self.ForceMethod('GET')
        return self.cM_Users.ListAllUsers()
    
    def GetUser(self):
        self.ForceMethod('GET')
        email = self.GetParam('email')
        return self.cM_Users.GetUserByEmail(email)
        

    def CreateUser(self):
        return "bye"