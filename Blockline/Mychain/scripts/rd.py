'''
Buy the coin on Koinex with minimum rate_diff.
Sell the coin on KOinex with maximum rate_diff.
'''
import urllib, json
import datetime
import urllib.request
from django.http import HttpResponse,JsonResponse

class RateDif:
    def __init__(self):
        self.koinex = "https://koinex.in/api/ticker"
        self.zebpay = "https://www.zebapi.com/api/v1/market/"
        self.cmk = "https://api.coinmarketcap.com/v1/ticker?convert=INR&limit=50" 
        self.date = datetime.date.today().strftime('%d-%m-%Y')
        self.time = datetime.datetime.now().time().strftime('%I:%M %p')
     
   
    def cal(self):
        try:
            k_response = []
            z_response = []
            
            koinex_response = urllib.request.urlopen(self.koinex).read()
            cmk_response = urllib.request.urlopen(self.cmk).read()
            
            koinex_json = json.loads(koinex_response)
            cmk_json = json.loads(cmk_response)
             
            for coin,price in koinex_json['prices']['inr'].items():
               for items in cmk_json:
                   if ( items['symbol'] == coin and float(price) != 0):
                        perc_diff = ((float(price) - float(items['price_inr']))/float(price))*100
                        
                        k_response.append({
                            "id" : coin,
                            "koinex_price" : price,
                            "global_price" : items['price_inr'],
                            "rate_diff" : int(perc_diff), 
                            "timestamp" : self.date+' '+self.time,
                            })
                       
   
            list = ['BTC','XRP','EOS','LTC','ETH','BCH','OMG','TRX','GNT','ZRX']
            for items in cmk_json:
                if ( items['symbol'] in list):
                    zp_response = urllib.request.urlopen(self.zebpay+'ticker-new/'+ items['symbol'] +'/inr').read()
                    zp_json = json.loads(zp_response)
                    if float(zp_json['market'] != 0 ):
                        perc_diff = ((float(zp_json['market']) - float(items['price_inr']))/float(zp_json['market']))*100
                        
                    z_response.append({
                        "id" :items['symbol'] ,
                        "zebpay_price" : zp_json['market'] ,
                        "global_price" : items['price_inr'],
                        "rate_diff" : int(perc_diff),
                        "timestamp" : self.date+' '+self.time,
                        })
            
            return k_response , z_response

        except Exception as e:
            HttpResponse('Error !! ' , e)     
       
    
obj = RateDif()


def api_rd(request, ex=' '):
    koi , zeb =  obj.cal()
    if ex == 'z' :
        response = {'zebpay' : zeb }
    elif ex == 'k' : 
        response = {'koinex' : koi }
    else : 
        response = {
                'zebpay' : zeb ,
                'koinex' : koi , 
                }
    return JsonResponse(response, safe=False)

