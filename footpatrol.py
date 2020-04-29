from urllib.request import urlopen as uReq
from urllib.request import Request
from selenium import webdriver
import requests
headers = {
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}

# request part
my_url = requests.get("https://www.footpatrol.com/campaign/New+In/brand/jordan/?facet-new=latest",headers=headers)

print(my_url.status_code)
'''
uClient=uReq(my_url)
page_html=uClient.read()
uClient.close()
print(page_html)
'''
