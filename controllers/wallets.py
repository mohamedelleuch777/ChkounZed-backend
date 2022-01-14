import config

class Wallets( config.Controller ) :
    cM_Wallets = None
    def __init__ (self):
        self.cM_Wallets = config.importModule("models/M_Wallets").M_Wallets()
        
