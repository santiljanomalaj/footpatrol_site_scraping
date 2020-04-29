from selenium import webdriver
from lxml import html
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as soup
from dhooks import Webhook, Embed
from random import randint
import time
import re
import pymysql
import time, threading

# retrieve proxy IP addresses from proxies.txt file
proxies = open("proxies.txt", "rt")
proxy = proxies.read()         
proxies.close()                   
proxy_list = proxy.split("\n")

#Connection to MYSQL DB
conn=pymysql.connect(host="localhost",user="root",password="",db="footpatrol")
c=conn.cursor()

# set discord wehook url
hook = Webhook("https://discordapp.com/api/webhooks/703451120327983224/SosLLsdSOKc-qptPqFI3CdZtqbJDQ5hcDTo7befaf8-bvaAiRCNXr203lV6lBY4G87x8")
# hook = Webhook("https://discordapp.com/api/webhooks/703723259316928573/LxTBMSJ5SOzfnd_fPyNOgWH24FzWVr_iLUU2d6t5TiecrNvCvj7UavXyWRUUCNmj49CK")


def get_product():

  # get proxy_ip
  random_index = randint(0, len(proxy_list))
  proxy_ip=get_proxies(random_index)

  # set proxy
  options = Options()
  options.add_argument("--prox-server=%s" % proxy_ip)
  options.add_argument("--window-size=1466,868")
  options.add_argument("--disable-notifications")
  options.add_argument("--lang=en")

  # run chromdriver
  # driver = webdriver.Chrome(chrome_options=options)
  driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
  # driver = webdriver.Chrome()

  time.sleep(2)
  driver.delete_all_cookies()
  time.sleep(2)
  driver.get('https://www.footpatrol.com/campaign/New+In/?facet:new=latest&sort=latest')

  response=driver.page_source
  products=soup(response, 'html.parser')


  product_totalNum=products.find('div',{'class':'pageCount'}).text
  productNum=re.findall('\d+', product_totalNum )
  pageNum=int((int(productNum[0]))/24)
  # product list and product item
  for page in range(pageNum):
    if page==0:
      productUrl_lists=products.find('ul',{'id':'productListMain'}).findAll('span',{'class', 'itemContainer'})
    else:
      driver.delete_all_cookies()
      time.sleep(1)
      driver.get('https://www.footpatrol.com/campaign/New+In/latest/?facet-new=latest&fp_sort_order=latest&from='+str(page*24))

      response=driver.page_source
      products=soup(response, 'html.parser')
      productUrl_lists=products.find('ul',{'id':'productListMain'}).findAll('span',{'class', 'itemContainer'})
    for product_url in productUrl_lists:
      #product item info
      product_link='https://www.footpatrol.com'+product_url.a['href']

      driver.delete_all_cookies()
      driver.get(product_link)

      time.sleep(5)
      products_response=driver.page_source
      products_info=soup(products_response, 'html.parser')

      product_link_number=product_link.split('/')
      product_id = re.findall('\d+', product_link_number[5] )
      product_name=products_info.find('div',{'id':'productItemTitle'}).h1.text
      product_price=products_info.find('div',{'class':'itemPrices'}).span.text
      product_img=products_info.find('button',{'class':'owl-thumb-item active'}).picture.img['src']
      product_size=products_info.find('div',{'id':'productSizeStock'}).findAll('button')

      product_item_size=""

      for item_size in product_size:
        product_item_size+='\n'+re.sub("\s\s+"," ",item_size.text.replace('Learn More',''))
      product_brand=re.findall('\\bYeezy\\b', product_name)
      if(len(product_brand)==0):
        product_brand=re.findall('\\bJordan\\b', product_name)
      if(product_item_size==""):
        product_item_size="not size"
      if (('Yeezy' in product_name) or ('Jordan' in product_name)):
        print(product_img+","+product_price+","+product_brand[0]+","+product_name+","+product_item_size+","+product_id[0]+","+product_link+"\n")

        # compare new product and old product, insert new product into database
        c.execute("SELECT * from product WHERE product_id=%s",product_id[0])
        products=c.fetchall()
        if len(products):
          continue
        c.execute("""INSERT into product(brand,product_id) VALUES (%s,%s)""",(product_brand[0],product_id[0]))
        conn.commit()

        #send the product_data into discord webhook
        embed = Embed(
            color=0x1E90FF,
            timestamp="now"
            )
        embed.set_author(name=product_id[0]+" + new product "+product_brand[0])
        embed.add_field(name="product url", value=product_link)
        embed.set_footer(text="Astro AP")
        hook.send(embed=embed)
        embeded = Embed(
            color=0x1E90FF,
            timestamp="now"
            )
        embeded.set_author(name=product_name)
        embeded.add_field(name="product size", value=product_item_size)
        embeded.add_field(name="product price", value=product_price)
        embeded.set_footer(text="Astro AP")
        embeded.set_thumbnail(product_img)
        hook.send(embed=embeded)
      
  driver.quit()  
  threading.Timer(600, get_product).start()
def get_proxies(index): 
  return proxy_list[index]
get_product()
