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
        self.new_cmk = "https://api.coinmarketcap.com/v2/ticker/?sort=rank&convert=INR&limit=50"
        self.date = datetime.date.today().strftime('%d-%m-%Y')
        self.time = datetime.datetime.now().time().strftime('%I:%M %p')
        self.cmk_response = urllib.request.urlopen(self.cmk).read()
        self.cmk_json = json.loads(self.cmk_response)
        self.new_cmk_response = urllib.request.urlopen(self.new_cmk).read()
        self.new_cmk_json = json.loads(self.new_cmk_response)
        
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
                            "market_price": zi['market'],
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
                            "market_price": zi['market'],
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
                self.zeb_coins.add(zi['virtualCurrency'])
            return True
        except Exception as e:
            return False

    def calNewZebpay(self,market):
        market = market.upper()
        try:
            inr_z_response = {}
            btc_z_response = {}
            #coins  = ['BTC','BCH','LTC','XRP','EOS','OMG','TRX','GNT','ZRX','REP','KNC','BAT','VEN','AE','ZIL','CMT','NCASH']
            
            for i in self.zeb_coins: 
                if market != i : 
                    url = self.new_zebpay + i + '/' + market
                    zebpay_req = urllib.request.Request(url , headers = {'User-Agent':'Mozilla/5.0'})
                    zebpay_response = urllib.request.urlopen(zebpay_req).read()
                    coin = json.loads(zebpay_response)
                    for j,k in self.new_cmk_json['data'].items():
                        if i == k['symbol'] and coin['market'] != 0 : 
                            buy_perc_diff = int(( (float(coin['buy']) - float(k['quotes'][market]['price'])) / float(coin['buy']) ) *100 )
                            sell_perc_diff = int(( (float(coin['sell']) - float(k['quotes'][market]['price'])) / float(coin['sell']) ) *100 )
                        
                            if market == 'INR' : 
                                inr_z_response.update({
                                    i : {
                                    "buy_diff" : buy_perc_diff,
                                    "sell_diff" : sell_perc_diff,
                                    "market_price": coin['market'],
                                    "global_price" : k['quotes'][market]['price'],
                                    "timestamp" : self.date+' '+self.time,
                                    }})
                            elif market == 'BTC' :
                                btc_z_response.update({
                                    i : {
                                    "buy_diff" : buy_perc_diff,
                                    "sell_diff" : sell_perc_diff,
                                    "market_price": coin['market'],
                                    "global_price" : k['quotes'][market]['price'],
                                    "timestamp" : self.date+' '+self.time,
                                    }})
                           
            if market == 'INR' :
                return inr_z_response
            elif market == 'BTC' :
                return btc_z_response
            else:
                return inr_z_response,btc_z_response
     
        except Exception as e:
             return {"error":str(e)}


    def cal_bitbns(self):
        try:
            bitbns_res = {}
            bitbns_request = urllib.request.Request(self.bitbns , headers={'User-Agent':'Mozilla/5.0'})
            bitbns_response = urllib.request.urlopen(bitbns_request).read()
            bitbns_json = json.loads(bitbns_response)

            for coin,data in bitbns_json.items() :
                for rank,values in self.new_cmk_json['data'].items() :
                    if values['symbol'] == coin and int(data['lowest_sell_bid']) != 0 and int(data['highest_buy_bid']) != 0 :
                        buy_diff = int(( (float(data['lowest_sell_bid']) - float(values['quotes']['INR']['price']) )/ float(data['lowest_sell_bid']) )*100)
                        sell_diff = int(( (float(data['highest_buy_bid']) - float(values['quotes']['INR']['price']) )/ float(data['highest_buy_bid']) )*100)
                        res = {
                            "buy_diff" : str(buy_diff),
                            "sell_diff" : str(sell_diff), 
                            "market_price" : data['last_traded_price'],
                            "global_price" : str(values['quotes']['INR']['price']),
                            "timestamp" : self.date+' '+self.time,
                            }
                        bitbns_res.update({coin : res})
            return bitbns_res

        except Exception as e:
            return {"error":str(e)}


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
                inr_zeb, btc_zeb = obj.cal_zebpay()
                #btc_zeb = obj.calNewZebpay('BTC')
                #inr_zeb = obj.calNewZebpay('INR')
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
