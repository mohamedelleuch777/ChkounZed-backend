import config


class Users : 
    
    
    def run(self):
        return config.REQUEST_ARGS
    
    def GetUser(self):
        return config.GetPostArgs()