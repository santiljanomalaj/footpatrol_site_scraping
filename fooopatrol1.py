from selenium import webdriver
from lxml import html
import time
from bs4 import BeautifulSoup as soup
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

driver.get('https://www.footpatrol.com/campaign/New+In/?facet:new=latest&sort=latest')

response=driver.page_source
products=soup(response, 'html.parser')

productUrl_lists=products.find('ul',{'id':'productListMain'}).findAll('span',{'class', 'itemContainer'})

product_url='https://www.footpatrol.com'+productUrl_lists[0].a['href']

driver.get(product_url)
# for product_url in productUrl_lists:
  # driver.get()

# driver.quit()