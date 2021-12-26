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