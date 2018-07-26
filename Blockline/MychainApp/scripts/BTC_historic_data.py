import urllib.request,json,os,csv,datetime

class hData:
	def __init__(self):
		self.cur_date = datetime.date.today().strftime('%Y-%m-%d')
		self.coindesk_url = 'https://api.coindesk.com/v1/bpi/historical/close.json?'+ urllib.parse.urlencode({'currency':'INR','start':'2011-01-01','end':self.cur_date})
		 

	def histdata(self):
		file=open('histdata.csv','w')
		try:
			cd_response = urllib.request.urlopen(self.coindesk_url).read()
			cd_json_data = json.loads(cd_response)
			cd_data = cd_json_data['bpi']
			csvwriter = csv.writer(file)
			csvwriter.writerow(cd_data.items())
	
		except Exception as e:
			file.write('<br>Error!! '+ str(e))
		file.close()

if __name__ == '__main__':
	hdata_obj = hData()
	hdata_obj.histdata()

