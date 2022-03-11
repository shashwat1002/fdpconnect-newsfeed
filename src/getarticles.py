from imo import links
# from imo import dummy
from selenium.webdriver.common.by import By 
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import pandas as pd
import sys
import os
from selenium.webdriver.common.keys import Keys
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
url="https://www.thehindu.com/"
d=[]
l=[]
name=[]
driver.get(url)
no_of_pages=0
try:
    x=driver.find_element_by_class_name("e-load-more-anchor")
    no_of_pages=int(x.get_attribute("data-max-page"))
    print(no_of_pages)
except:
    pass

page_url_start="https://www.thehindu.com/business/Industry/"
article_urls=[]

for i in range(1,no_of_pages+1):
    cur_url=page_url_start+str(i)+'/'
    driver = webdriver.Firefox(options=options)
    driver.get(cur_url)
    urls=driver.find_elements_by_class_name("elementor-post__thumbnail__link")
    
    for url in urls:
        article_urls.append(url.get_attribute("href"))
print(len(article_urls))




def getdata(url):
    driver.get(url)
    try:
        x=driver.find_elements_by_class_name("elementor-widget-theme-post-content")
        x=x[0].find_elements_by_class_name("elementor-widget-container")
        
        temp=x[0].find_elements_by_tag_name("p")
       
        t=""
        for a in temp:
            t=t+a.text+" " 
        d.append(t)
    except:
        d.append("Nan")
    
    
# getdata(url)
cnt=1

for url in article_urls:
    l.append(url)

    print(cnt)
    getdata(url)
    cnt+=1


data = list(zip(l,d))
# print(data)
df = pd.DataFrame(data,columns=['links','article'])
df.to_csv('articldata.csv')
