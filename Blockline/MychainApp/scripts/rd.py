'''
Buy the coin with minimum sell rate_diff.
Sell the coin with maximum buy rate_diff.
'''
import urllib, json
import datetime
import urllib.request
from django.http import JsonResponse

class RateDif(object):
    def __init__(self):
        self.bitbns = "https://bitbns.com/order/getTickerWithVolume/"
        self.koinex = "https://koinex.in/api/ticker"
        self.zebpay = "https://www.zebapi.com/api/v1/market/"
        self.new_zebpay = "https://www.zebapi.com/api/v1/market/ticker-new/"
        self.cmk = "https://api.coinmarketcap.com/v1/ticker?convert=INR&limit=60" 
        self.new_cmk = "https://api.coinmarketcap.com/v2/ticker/?sort=rank&convert=INR&limit=100"
        self.date = datetime.date.today().strftime('%d-%m-%Y')
        self.time = datetime.datetime.now().time().strftime('%I:%M %p')
        self.cmk_response = urllib.request.urlopen(self.cmk).read()
        self.cmk_json = json.loads(self.cmk_response)
        self.new_cmk_response = urllib.request.urlopen(self.cmk).read()
        self.new_cmk_json = json.loads(self.cmk_response)
        
        self.zeb_coins = set()
        #self.getZebpayCoins()
        if self.getZebpayCoins() is False:
            self.zeb_coins  = ['BTC','BCH','LTC','XRP','EOS','OMG','TRX','GNT','ZRX','REP','KNC','BAT','VEN','AE','ZIL','CMT','NCASH']

    def cal_koinex(self):
        try:
            k_response = {}
            koinex_response = urllib.request.urlopen(self.koinex).read()
            koinex_json = json.loads(koinex_response)
            
            for coin,price in koinex_json['prices']['inr'].items():
               for items in self.cmk_json:
                   if  items['symbol'] == coin and float(price) != 0 :
                        perc_diff = ((float(price) - float(items['price_inr'])) / float(price))*100
                        
                        k_response.update({coin:{
                            "koinex_price" : price,
                            "global_price" : items['price_inr'],
                            "rate_diff" : int(perc_diff), 
                            "timestamp" : self.date+' '+self.time,
                            }})
            return k_response 

        except Exception as e:
            return {"error":str(e)}


    def cal_zebpay(self):
        try:
            inr_z_response = {}
            btc_z_response = {}
            zebpay_req = urllib.request.Request(self.zebpay, headers = {'user-agent':'Mozilla/5.0'})
            zebpay_response = urllib.request.urlopen(zebpay_req).read()
            zebpay_json = json.loads(zebpay_response)
            
            for zi in zebpay_json:
                for ci in self.cmk_json:
                    
                    if (zi['pair'])[:3] == ci['symbol'] and (zi['pair'])[4:]=='INR' and float(zi['buy']) != 0 :
                        #inr_perc_diff = ((float(zi['buy']) - float(ci['price_inr'])) / float(zi['buy']))*100
                        inr_buy_perc_diff = int((( float(zi['buy']) - float(ci['price_inr'])) /  float(zi['buy']) ) *100 )
                        inr_sell_perc_diff = int((( float(zi['sell']) - float(ci['price_inr'])) /  float(zi['sell']) ) *100 )
                        inr_z_response.update({ci['symbol'] : {
                            "buy_diff" : str(inr_buy_perc_diff) ,
                            "sell_diff" : str(inr_sell_perc_diff),
                            "global_price" : ci['price_inr'],
                            "timestamp" : self.date+' '+self.time,
                            }})
                    
                    if (zi['pair'])[:3] == ci['symbol'] and (zi['pair'])[4:]=='BTC' and float(zi['buy']) != 0 :
                        #btc_perc_diff = ((float(zi['buy']) - float(ci['price_btc'])) / float(zi['buy']))*100
                        btc_buy_perc_diff = int((( float(zi['buy']) - float(ci['price_btc'])) /  float(zi['buy']) ) *100 )
                        btc_sell_perc_diff = int((( float(zi['sell']) - float(ci['price_btc'])) /  float(zi['sell']) ) *100 )
                        btc_z_response.update({ci['symbol'] : {
                            "buy_diff" : str(btc_buy_perc_diff) ,
                            "sell_diff" : str(btc_sell_perc_diff),
                            "global_price" : ci['price_btc'],
                            "timestamp" : self.date+' '+self.time,
                            }})
     
            if inr_z_response and btc_z_response :
                return inr_z_response, btc_z_response
            elif not inr_z_response:
                return btc_z_response, 'not available'
            elif not btc_z_response:
                return inr_z_response, 'not available'
                
        except Exception as e:
             return {"error":str(e)}

    def getZebpayCoins(self):
        try:
            zebpay_req = urllib.request.Request(self.zebpay, headers = {'user-agent':'Mozilla/5.0'})
            zebpay_response = urllib.request.urlopen(zebpay_req).read()
            zebpay_json = json.loads(zebpay_response)
            for zi in zebpay_json:
                zeb_coins.add(zi['virtualCurrency'])
            return True
        except Exception as e:
            return False

    def calNewZebpay(self,market='INR'):
        market = market.upper()
        try:
            inr_z_response = {}
            btc_z_response = {}
            #coins  = ['BTC','BCH','LTC','XRP','EOS','OMG','TRX','GNT','ZRX','REP','KNC','BAT','VEN','AE','ZIL','CMT','NCASH']
            
            for i in self.zeb_coins: 
                if market != i : 
                    url = self.new_zebpay + i + '/' + market
                    print(url)
                    zebpay_req = urllib.request.Request(self.new_zebpay, headers = {'user-agent':'Mozilla/5.0'})
                    print(zebpay_req)
                    zebpay_response = urllib.request.urlopen(zebpay_req).read()
                    print(zebpay_response)
                    coin = json.loads(zebpay_response)
                    for j,k in self.new_cmk_json['data'].items():
                        if i is k['symbol'] and coin['market'] != 0 : 
                        
                            buy_perc_diff = int(( (float(coin['buy']) - float(k['quotes'][market]['price'])) / float(coin['buy']) ) *100 )
                            sell_perc_diff = int(( (float(coin['sell']) - float(k['quotes'][market]['price'])) / float(coin['sell']) ) *100 )
                        
                            if market is 'INR' : 
                                inr_z_response.update({
                                    "coin" : {
                                    "buy_diff" : buy_perc_diff,
                                    "sell_diff" : sell_perc_diff,
                                    "global_price" : k['quotes'][market]['price'],
                                    "timestamp" : self.date+' '+self.time,
                                    }})
                            elif market is 'BTC' :
                                btc_z_response.update({
                                    "coin" : {
                                    "buy_diff" : buy_perc_diff,
                                    "sell_diff" : sell_perc_diff,
                                    "global_price" : k['quotes'][market]['price'],
                                    "timestamp" : self.date+' '+self.time,
                                    }})
                            else : 
                                inr_z_response.update({
                                    "coin" : {
                                    "buy_diff" : buy_perc_diff,
                                    "sell_diff" : sell_perc_diff,
                                    "global_price" : k['quotes'][market]['price'],
                                    "timestamp" : self.date+' '+self.time,
                                    }})
                                btc_z_response.update({
                                    "coin" : {
                                    "buy_diff" : buy_perc_diff,
                                    "sell_diff" : sell_perc_diff,
                                    "global_price" : k['quotes'][market]['price'],
                                    "timestamp" : self.date+' '+self.time,
                                    }})
                        #For XYZ/XYZ coin situation
                        else:
                             if market is 'INR' :
                                inr_z_response.update({i : "not found"})
                             elif market is 'BTC' :
                                btc_z_response.update({i : "not found"})
            if market is 'INR' :
                return inr_z_response
            elif market is 'BTC' :
                return btc_z_response
            else:
                return inr_z_response,btc_z_response
     
        except Exception as e:
             return {"error":str(e)}


    def cal_bitbns(self):
        try:
            bitbns_res = {}
            bitbns_request = urllib.request.Request(self.bitbns , headers={'User-Agent': 'Mozilla/5.0'})
            bitbns_response = urllib.request.urlopen(bitbns_request).read()

            for coins in bitbns_response :
                for items in self.cmk_json :
                    if float(bitbns_response[coins]['last_traded_price']) != 0  :
                        perc_diff = ( (bitbns_response[coins]['last_traded_price'] - float(items['price_inr']) ) / float(bitbns_response[coins]['last_traded_price']) )*100
                        
                        bitbns_res.update({coins:{
                            "bitbns_price" : bitbns_response[coins]['last_traded_price'],
                            "global_price" : items['price_inr'],
                            "rate_diff" : str(perc_diff), 
                            "timestamp" : self.date+' '+self.time,
                            }})
            return bitbns_res

        except Exception as e:
            return {"error":str(e)}


#Get list of coin in zebpay
#if __name__ == '__main__':
#    obj = RateDif()
#    obj.getZebpayCoins()
#    if obj.getZebpayCoins() is False:
#         obj.zeb_coins  = ['BTC','BCH','LTC','XRP','EOS','OMG','TRX','GNT','ZRX','REP','KNC','BAT','VEN','AE','ZIL','CMT','NCASH']



#Creating APIs
def api_rd(request, ex=' ' , mk=' '):
    try:
        obj = RateDif()
        if ex == 'z' :
            #inr_zeb, btc_zeb = obj.cal_zebpay()
          
            if mk == 'btc' or mk == 'BTC':
                btc_zeb = obj.calNewZebpay(mk)
                response = {'zebpay' : {'btc_market' : btc_zeb}
                                    }
            elif mk == 'inr' or mk == 'INR':
                inr_zeb = obj.calNewZebpay(mk)
                response = {'zebpay' : {'inr_market' : inr_zeb}
                                    }
            else :
                inr_zeb, btc_zeb = obj.calNewZebpay(mk)
                response = {'zebpay' : {'inr_market' : inr_zeb, 
                                    'btc_market' : btc_zeb}
                                    }
   
        elif ex == 'k' : 
            koi =  obj.cal_koinex()
            response = {'koinex' : koi }

        
        elif ex == 'b' : 
            bitbns =  obj.cal_bitbns()
            response = {'bitbns' : bitbns }
   
        else : 
            inr_zeb, btc_zeb = obj.cal_zebpay()
            koi =  obj.cal_koinex()
            response = {
                    'zebpay' : {'inr_market' : inr_zeb, 
                                'btc_market' : btc_zeb
                                } ,
                    'koinex' : koi , 
                    }
        return JsonResponse(response, safe=False)

    except Exception as e:
        res = { 'Error' : str(e) }
        return JsonResponse(res, safe=False) 
