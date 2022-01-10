import config
import mysql.connector
import time
import sql

class M_Transactions : 
    connDB = None
    db = None
    def __init__ (self):
        self.connDB = mysql.connector.connect(
            host="remotemysql.com",
            user="O4pKtnrYIk",
            password="hd0iDziUDK",
            database="O4pKtnrYIk"
        )
        self.db = sql.Sql()

    def ListAllTxPerItemCore(self, user_id, item_id, page, pageSize):
        mycursor = self.connDB.cursor()
        mycursor.execute("SELECT * FROM `Transactions` WHERE `maker_user_id` = "+str(user_id)+" AND `item_id` = "+str(item_id)+" AND `tx_type` = 'bid' LIMIT "+str(page)+" OFFSET "+str(pageSize))
        return mycursor.fetchall()

    def ListAllTxWalletCore(self, user_id, page, pageSize):
        mycursor = self.connDB.cursor()
        mycursor.execute("SELECT * FROM `Transactions` WHERE `maker_user_id` = "+str(user_id)+" AND `tx_type` = 'wallet+' AND `tx_type` = 'wallet-' LIMIT "+str(page)+" OFFSET "+str(pageSize))
        return mycursor.fetchall()

    def MakeBidCore(self, user_data, item_id, bid_amount):
        # getting user status:
        user_id = user_data[0][0]
        user_status = user_data[0][9]
        # is user banned
        banned = config.isFlagActive(user_status, config.constants.FLAG_BANNED)
        if banned:
            config.ReturnJsonError("Banned user cannot bid")
        # getting user wallet:
        mycursor = self.connDB.cursor()
        mycursor.execute("SELECT * FROM `Wallet` WHERE `user_id` = "+str(user_id))
        res = mycursor.fetchall()
        user_wallet = res[0]
        user_total_balance = user_wallet[4]
        # check user balance and user requested bid:
        if ( bid_amount <= 0 or bid_amount>user_total_balance):
            config.ReturnJsonError("bid amount should be geater than 0 and should not exceed the balance")
        # passed all tests successfully
        # continue here
        # save tx to db
        ts = int(time.time() * 1000)
        cols = ["id"    ,"tx_type"  ,"amount"   ,"status","timestamp","maker_user_id","taker_user_id","item_id"]
        vals = ["NULL"  ,"bid"      , str(bid_amount),"4"     , str(ts)        , str(user_id)       , str(0)             ,str(item_id)]
        self.db.Insert("Transactions",cols,vals)
        return {
            "success": True,
            "message": "bid placed for that item"
        }


