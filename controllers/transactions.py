import config

class Transactions( config.Controller ) :
    cM_Transactions = None
    def __init__ (self):
        self.cM_Transactions = config.importModule("models/M_Transactions").M_Transactions()
        self.cM_Users = config.importModule("models/M_Users").M_Users()
        self.cM_Items = config.importModule("models/M_Items").M_Items()
        self.cM_Wallets = config.importModule("models/M_Wallets").M_Wallets()
        
    def run(self):
        return config.REQUEST_ARGS
        
    def GetUserTxPerItem(self):
        self.ForceMethod('GET')
        bearerToken = self.GetBearerToken() # will throw a 401 exception if token is not valid or if its expired
        id = self.GetDataFromToken(bearerToken,'id')
        page = self.GetGetArgs('page')
        item = self.GetGetArgs('item_id')
        pageSize = self.GetGetArgs('page_size')
        pageSize = pageSize if pageSize else 10
        return self.cM_Transactions.ListAllTxPerItemCore(id, item, page, pageSize)
        
    def GetUserTxWallet(self):
        self.ForceMethod('GET')
        bearerToken = self.GetBearerToken() # will throw a 401 exception if token is not valid or if its expired
        id = self.GetDataFromToken(bearerToken,'id')
        page = self.GetGetArgs('page')
        pageSize = self.GetGetArgs('page_size')
        pageSize = pageSize if pageSize else 10
        return self.cM_Transactions.ListAllTxWalletCore(id, page, pageSize)
        
    def MakeBid(self):
        self.ForceMethod('POST')
        bearerToken = self.GetBearerToken() # will throw a 401 exception if token is not valid or if its expired
        id = self.GetDataFromToken(bearerToken,'id')
        args = self.GetPostArgs()
        item_id = args['item_id']
        bid_amount = args['bid_amount']
        user = self.cM_Users.GetUserData(id)
        # getting user status and id:
        user_id = user[0][0]
        user_status = user[0][9]
        item_accept_bids = self.cM_Items.DoesItemAcceptBid(item_id)
        balance = self.cM_Wallets.GetUserBalance(user_id)
        # is user banned
        banned = config.isFlagActive(user_status, config.constants.FLAG_BANNED)
        if banned:
            config.ReturnJsonError("Banned user cannot bid")
        # is item accepting bids
        if not item_accept_bids:
            config.ReturnJsonError("This item does not accept bids at the moment")
        if len(user)==0: 
            config.ReturnJsonError("Error while reading user data")
        # check user balance and user requested bid:
        if ( bid_amount <= 0 or bid_amount>balance):
            config.ReturnJsonError("bid amount should be geater than 0 and should not exceed the balance")
        # call make bid core function
        self.cM_Transactions.MakeBidCore(user_id,item_id,bid_amount,balance)
        # deduct bid from balance
        new_balance = balance - bid_amount
        self.cM_Wallets.SetUserBalance(str(user_id),str(new_balance))
        return {
            "success": True,
            "message": "bid placed for that item"
        }
        