from urllib.request import urlopen as uReq
from urllib.request import Request


# request part
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'}
my_url = Request("https://www.footpatrol.com/campaign/New+In/brand/jordan/?facet-new=latest", headers=headers)
uClient=uReq(my_url)
page_html=uClient.read()
uClient.close()
print(page_html)
