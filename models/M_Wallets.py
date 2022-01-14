import config
import sql

class M_Wallets : 
    db = None
    def __init__ (self):
        self.db = sql.Sql()

    # getting user wallet:
    def GetUserWallet(self, user_id):
        return self.db.Select('Wallet',"`user_id` = "+str(user_id))

    # getting user balance:
    def GetUserBalance(self, user_id):
        wallet = self.GetUserWallet(user_id)[0]
        return wallet[4]

    # setting user balance:
    def SetUserBalance(self, user_id, new_balance):
        self.db.Update('Wallet','total_balance',new_balance,"`user_id` = "+str(user_id))

    # getting user currency:
    def GetUserWCurrency(self, user_id):
        wallet = self.GetUserWallet(user_id)[0]
        return wallet[2]

    # getting user currency symbol:
    def GetUserWCurrencySymbol(self, user_id):
        wallet = self.GetUserWallet(user_id)[0]
        return wallet[3]