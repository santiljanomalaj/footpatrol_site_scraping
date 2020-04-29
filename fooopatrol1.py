from selenium import webdriver
from lxml import html
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as soup
from dhooks import Webhook, Embed
import time
import re
import pymysql

#Connection to MYSQL DB
conn=pymysql.connect(host="localhost",user="root",password="",db="offspring")
c=conn.cursor()

# set discord wehook url
hook = Webhook("https://discordapp.com/api/webhooks/703451120327983224/SosLLsdSOKc-qptPqFI3CdZtqbJDQ5hcDTo7befaf8-bvaAiRCNXr203lV6lBY4G87x8")
# hook = Webhook("https://discordapp.com/api/webhooks/703723259316928573/LxTBMSJ5SOzfnd_fPyNOgWH24FzWVr_iLUU2d6t5TiecrNvCvj7UavXyWRUUCNmj49CK")

# run chromdriver
driver = webdriver.Chrome()

driver.get('https://www.footpatrol.com/campaign/New+In/?facet:new=latest&sort=latest')

response=driver.page_source
products=soup(response, 'html.parser')

productUrl_lists=products.find('ul',{'id':'productListMain'}).findAll('span',{'class', 'itemContainer'})


#product item info
product_url='https://www.footpatrol.com'+productUrl_lists[0].a['href']

print(product_url)  # https://www.footpatrol.com/product/black-medicom-vcd-andre-ball/354667_footpatrolcom/

driver.delete_all_cookies()
driver.get(product_url)
products_response=driver.page_source
products_info=soup(products_response, 'html.parser')

product_id = re.findall('\d+', product_url )
product_name=products_info.find('div',{'id':'productItemTitle'}).h1.text
product_price=products_info.find('div',{'class':'itemPrices'}).span.text
product_img=products_info.find('button',{'class':'owl-thumb-item active'}).picture.img['src']
product_size=products_info.find('div',{'class':'productSizeStock'}).findAll('button')

product_item_size=''

for item_size in product_size:
  product_item_size+='\n'+item_size.text
product_brand=re.findall('\\bYeezy\\b', product_name)
if(len(product_brand)==0):
  product_brand=re.findall('\\bJordan\\b', product_name)

if (('Yeezy' in product_name) or ('Jordan' in product_name)):
  print(product_img+","+product_price+","+product_brand+","+product_name+","+product_item_size+","+product_id+","+product_url)

  # compare new product and old product, insert new product into database
  c.execute("SELECT * from product WHERE product_id=%s",product_id)
  products=c.fetchall()
  # if len(products):
  #   continue
  c.execute("""INSERT into product(brand,product_id) VALUES (%s,%s)""",(product_brand,product_id))
  conn.commit()

# for product_url in productUrl_lists:
  # driver.get()

# driver.quit()