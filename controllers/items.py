import config

class Items( config.Controller ) :
    cM_Items = None
    def __init__ (self):
        self.cM_Items = config.importModule("models/M_Items").M_Items()
        
    def run(self):
        return config.REQUEST_ARGS
        
    def GetAllItems(self):
        self.ForceMethod('GET')
        return self.cM_Items.ListAllItems()
        
    def CreateItem(self):
        self.ForceMethod('POST')
        args = self.GetPostArgs()
        return self.cM_Items.CreateItemCore(args)

    def GetFutureItems(self):
        self.ForceMethod('GET')
        self.GetBearerToken() # will throw a 401 exeption if token is not valid or expired
        #args = self.GetPostArgs()
        args = config.REQUEST_ARGS
        ts = int(config.time.time() * 1000)
        count = args.split('=')[1]
        return self.cM_Items.ListFutureItemsCore(ts, count)

    def GetPastItems(self):
        self.ForceMethod('GET')
        self.GetBearerToken() # will throw a 401 exeption if token is not valid or expired
        #args = self.GetPostArgs()
        args = config.REQUEST_ARGS
        ts = int(config.time.time() * 1000)
        count = args.split('=')[1]
        return self.cM_Items.ListPastItemsCore(ts, count)