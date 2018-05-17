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
        self.cmk = "https://api.coinmarketcap.com/v1/ticker?convert=INR&limit=60" 
        self.date = datetime.date.today().strftime('%d-%m-%Y')
        self.time = datetime.datetime.now().time().strftime('%I:%M %p')
        self.cmk_response = urllib.request.urlopen(self.cmk).read()
        self.cmk_json = json.loads(self.cmk_response)


    def cal_koinex(self):
        try:
            k_response = []
            koinex_response = urllib.request.urlopen(self.koinex).read()
            koinex_json = json.loads(koinex_response)
            
            for coin,price in koinex_json['prices']['inr'].items():
               for items in self.cmk_json:
                   if  items['symbol'] == coin and float(price) != 0 :
                        perc_diff = ((float(price) - float(items['price_inr'])) / float(price))*100
                        
                        k_response.append({
                            "id" : coin,
                            "koinex_price" : price,
                            "global_price" : items['price_inr'],
                            "rate_diff" : int(perc_diff), 
                            "timestamp" : self.date+' '+self.time,
                            })
            return k_response 

        except Exception as e:
            return e





    def cal_zebpay(self):
        try:
            inr_z_response = []
            btc_z_response = []
            zebpay_response = urllib.request.urlopen(self.zebpay).read()
            zebpay_json = json.loads(zebpay_response)
            for zi in zebpay_json :
                for ci in self.cmk_json:
                    
                    if (zi['pair'])[:3] == ci['symbol'] and (zi['pair'])[4:]=='INR' and float(zi['buy']) != 0 :
                        inr_perc_diff = ((float(zi['buy']) - float(ci['price_inr'])) / float(zi['buy']))*100
                        inr_z_response.append({
                            "id" : ci['symbol'] ,
                            "zebpay_price" : zi['buy'] ,
                            "global_price" : ci['price_inr'],
                            "rate_diff" : int(inr_perc_diff),
                            "timestamp" : self.date+' '+self.time,
                            })
                    
                    if (zi['pair'])[:3] == ci['symbol'] and (zi['pair'])[4:]=='BTC' and float(zi['buy']) != 0 :
                        btc_perc_diff = ((float(zi['buy']) - float(ci['price_btc'])) / float(zi['buy']))*100
                        btc_z_response.append({
                            "id" : ci['symbol'] ,
                            "zebpay_price" : zi['buy'] ,
                            "global_price" : ci['price_btc'],
                            "rate_diff" : int(btc_perc_diff),
                            "timestamp" : self.date+' '+self.time,
                            })
            return inr_z_response, btc_z_response               
                        
        except Exception as e:
             return e 



def api_rd(request, ex=' ' , mk=' '):
    try:
        obj = RateDif()
        if ex == 'z' :
            inr_zeb, btc_zeb = obj.cal_zebpay()
            if mk == 'btc':
                response = {'zebpay' : {'btc_market' : btc_zeb}
                                    }
            elif mk == 'inr':
                response = {'zebpay' : {'inr_market' : inr_zeb}
                                    }
            else :
                response = {'zebpay' : {'inr_market' : inr_zeb, 
                                    'btc_market' : btc_zeb}
                                    }
   
        elif ex == 'k' : 
            koi =  obj.cal_koinex()
            response = {'koinex' : koi }
   
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
        return JsonResponse({'Error': e}) 
