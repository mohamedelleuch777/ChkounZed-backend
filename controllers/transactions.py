import config

class Transactions( config.Controller ) :
    cM_Transactions = None
    def __init__ (self):
        self.cM_Transactions = config.importModule("models/M_Transactions").M_Transactions()
        self.cM_Users = config.importModule("models/M_Users").M_Users()
        self.cM_Items = config.importModule("models/M_Items").M_Items()
        
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
        item_accept_bids = self.cM_Items.DoesItemAcceptBid(item_id)
        if not item_accept_bids:
            config.ReturnJsonError("This item does not accept bids at the moment")
        if len(user)==0: 
            config.ReturnJsonError("Error while reading user data")
        return self.cM_Transactions.MakeBidCore(user,item_id,bid_amount)
        