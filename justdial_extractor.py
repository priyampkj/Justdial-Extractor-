import requests
import csv
import os
from colorama import Fore , init
from concurrent.futures import ThreadPoolExecutor
import time
from pyfiglet import figlet_format
init()
def get_data(location,search_term,page):
	burp0_url = "https://t.justdial.com:443/api/india_api_write/05july2019/searchziva.php?city={}&area=&lat=&long=&darea_flg=0&case=spcall&stype=category_list&search={}&nextdocid=&attribute_values=&basedon=&sortby=&nearme=0&rnd1=0.67612&rnd2=0.52278&rnd3=0.68590&max=10&pg_no={}&wap=2&debugmode=1&pecounter=0&median_latitude=&median_longitude=&bd_text=&login_mobile=&search_option=0&sort_order=0&pricedesc=0&priceasc=0&checkin=&checkout=&attr_search=&opt=&dummy=0&querySieve=search&querySieve=checkout&querySieve=checkin&adword_pos=%7B%7D&locflg=0&view_flag=&sieve=%7B%22name%22%3A%22resultModel%22%2C%22selector%22%3A%22result%22%2C%22runInit%22%3Atrue%7D&seopage=&sHash=&dHash=&bdtextdata=&isgroup=&new=1&searchReferrer=gen%7Cauto%7Chmpge&utm_source=&utm_medium=&jdlite=1&jdliteversion=4.0".format(location,search_term,page)
	burp0_headers = {
	"Connection": "close",
	"User-Agent": "Mozilla/5.0 (Linux; Android 9; Samsung Galaxy S9 Build/PD1A.180720.031; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.158 Mobile Safari/537.36",
	"content-type": "application/json",
	"Accept": "*/*",
	"Referer": "https://t.justdial.com/Chandigarh",
	"Accept-Encoding": "gzip, deflate",
	"Accept-Language": "en-US",
	"X-Requested-With": "com.justdial.jdlite"
		 }
	r=requests.get(burp0_url, headers=burp0_headers)
	x=r.json()
	return x

def try_get_data(d,n):
	try:
		return d[str(n)]
	except:
		return ''
def add_to_csv(s,l,data):
	filename=s+' in '+l+'.csv'
	if not os.path.exists(filename):
		with open(filename,'a') as f:
			wr=csv.DictWriter(f,delimiter=';',fieldnames=['Name', 'Numbers', 'Address', 'Ratings', 'Latitude', 'Longitude', 'Total Reviews'])
			wr.writeheader()
		
	with open(filename,'a',newline='') as f:
		wr=csv.DictWriter(f,delimiter=';',fieldnames=['Name', 'Numbers', 'Address', 'Ratings', 'Latitude', 'Longitude', 'Total Reviews'])
		wr.writerow(data)

def run(s,l,p):
	pool=ThreadPoolExecutor(max_workers=5)
	tasks=[pool.submit(get_data,l,s,i+1) for i in range(p)]
	ctr=0
	for t in tasks:
		x=t.result()
		res=x['main']['data']
		for i in res:
			name=try_get_data(i,1)
			number=try_get_data(i,15)
			numbers=[]
			if number:
				try:
					if len(number['list']):
						for j in number['list']:
							numbers.append(j.split('_')[0])
					if len(number['vnumber']):
						numbers.append(umber['vnumber'])
				except:
					pass
			address=try_get_data(i,3)+'_'+try_get_data(i,12)
			rating=try_get_data(i,7)
			lat=try_get_data(i,4)
			longt=try_get_data(i,5)
			total_reviews=try_get_data(i,16)
			d={}
			d['Name']=name
			d['Numbers']=str(numbers)
			d['Address']=str(address)
			d['Ratings']=str(rating)
			d['Latitude']=str(lat)
			d['Longitude']=str(longt)
			d['Total Reviews']=total_reviews      
			add_to_csv(s,l,d)
			ctr+=1
			print(Fore.GREEN+name+'\t'+Fore.RED+str(numbers)+'\t'+Fore.GREEN+str(address))
			print(Fore.WHITE+'-'*100)
	return(ctr)
	

if __name__=='__main__':
	banner=figlet_format('Justdial Extractor')
	print(Fore.RED+'-'*50)
	print (Fore.GREEN+banner)
	print(Fore.RED+'-'*50)
	print(Fore.WHITE+'Contact :- priyampkj@gmail.com\n\nYou\'re solely Resposible for using the program!!')
	print(Fore.RED+'_'*50+Fore.WHITE+'\n')
	
	l=input('Enter City Name\t\t:-')
	s=input('Search Term\t:-')
	page_no=int(input('Upto Page No (Max 50)\t:-').strip())
	start_time=time.time()
	items=run(s,l,page_no)
	timetaken=time.time()-start_time
	print(Fore.WHITE+'{} Contacts'.format(items))
	print(Fore.WHITE+'Time Taken {} seconds'.format(timetaken))
	filename=s+' in '+l+'.csv'
	print('Saved As :- {}'.format(filename))

