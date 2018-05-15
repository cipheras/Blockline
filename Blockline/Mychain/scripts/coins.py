import urllib.request,json
from django.shortcuts import render
import datetime


class Coins:
    def __init__(self):
        self.baseurl = 'https://api.coinmarketcap.com/v1/ticker/'
        self.date = datetime.date.today().strftime('%d-%m-%Y')
        self.time = datetime.datetime.now().time().strftime('%I:%M %p')
        
    def data(self, cur, num):
        try:
            url = self.baseurl + '?' + urllib.parse.urlencode({'convert': cur ,'limit': num})
            response = urllib.request.urlopen(url).read()       
            data = json.loads(response)
            coin = [[] for _ in range(num)]
            for coins in range(num):
                coin[coins].append(str(data[coins]['rank']))
                coin[coins].append(str(data[coins]['name']))
                coin[coins].append(str(data[coins]['symbol']))
                coin[coins].append(round(float(data[coins]['price_'+ cur.lower()]),2))
                coin[coins].append(float(data[coins]['percent_change_1h']))
                coin[coins].append(float(data[coins]['percent_change_24h'])) 
                coin[coins].append(float(data[coins]['percent_change_7d']))
            
            return coin

        except Exception as e:
            print('<br>Error!! '+ str(e))


def show_coin(request):
    obj = Coins()
    num = request.POST.get('ncoin')
    cur = request.POST.get('cur')
    cur = 'INR' if cur is None or cur is '' else cur
    num = 10 if num is None or num is '' or int(num) > 400 else int(num)
    return render(request, 'index.html', {'date':obj.date,'time':obj.time,'coin':obj.data(cur,num),'cur':cur,'num':num})
    

