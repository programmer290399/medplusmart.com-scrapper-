import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar
import json 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time 
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common import exceptions  


# bar = IncrementalBar('Fetching Categories :',max = 2)

# out_file = open('category_links.json','w+' , encoding='ANSI')

# link_treasure_box = ['https://www.medplusmart.com/pharmaHome#DrugsbyTherapeutic','https://www.medplusmart.com/pharmaHome#surgicalProduct']

# links = list()
browser = None

try:
    browser = webdriver.Chrome()
except Exception as error:
    print(error)
# i = 0 
# for link in  link_treasure_box :
#     try:
#                 browser.get(link)
#                 html_text = browser.page_source

#     except Exception as err:
#                 print(str(err))
#                 break
#     else:
#                 print('\nSuccessfully Accessed:',link)

#     soup = None
#     if html_text is not None:
#             soup = BeautifulSoup(html_text, 'lxml')

#     if i == 0 : category_heads = soup.find('div',attrs={'id':"DrugsbyTherapeutic"}).find('ul', attrs={'class':"drugsCategory"}) ; i+=1 
#     else :  category_heads = soup.find('div',attrs={'id':"surgicalProduct"}).find('ul', attrs={'class':"drugsCategory"})
#     anchor_tags = category_heads.findChildren('a')
#     for tag in anchor_tags :
#         links.append('https://www.medplusmart.com'+tag.get('href', None))
#     bar.next()
        
# bar.finish()
# print('\n',len(links),'Links Recieved')


# print('Writing to file ....')
# json.dump({'links': list(set(links))},out_file)
# out_file.close()
# print('File successfully saved !!')

# links = json.loads(open('category_links.json','r' , encoding='ANSI').read())['links']
# out_file = open('medicine_links.json','w+' , encoding='ANSI')

# product_links = list()
# print('Fetching Medicines by category now ....')

# for link in links :
#     print('Working on :' ,link.split('/')[-3])
#     try:
#                 browser.get(link)
#                 html_text = browser.page_source

#     except Exception as err:
#                 print(str(err))
#                 break
#     else:
#                 print('Successfully Accessed:',link)
#                 print('Please be patient it may take several minutes .....')

#     soup = None
#     if html_text is not None:
#             soup = BeautifulSoup(html_text, 'lxml')
    
    
#     while True :
#         try :
#              element = browser.find_element_by_xpath('//*[@id="pagination"]/ul/li[8]/a')
#         except NoSuchElementException:
#             time.sleep(1)
#             html_text = browser.page_source
#             soup = BeautifulSoup(html_text, 'lxml')
#             anchor_tags = soup.find_all('a', attrs={"class":"text-default caps searchResultProductName"})
                
#             for tag in anchor_tags :
#                 product_links.append('https://www.medplusmart.com'+tag.get('href', None))
                    
#             break 
        
        
        
        
        
        
#         time.sleep(1)
#         element = WebDriverWait(browser, 120 ,ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,))\
#                         .until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '#pagination > ul > li:nth-child(8) > a')))
#         try :
#             if element.get_attribute("onclick") :
#                 time.sleep(1)
#                 html_text = browser.page_source
#                 soup = BeautifulSoup(html_text, 'lxml')
#                 anchor_tags = soup.find_all('a', attrs={"class":"text-default caps searchResultProductName"})
                
#                 for tag in anchor_tags :
#                     product_links.append('https://www.medplusmart.com'+tag.get('href', None))
                    
#                 browser.execute_script("arguments[0].click();", element)
#                 time.sleep(1)
#             else :
#                 time.sleep(1)
#                 html_text = browser.page_source
#                 soup = BeautifulSoup(html_text, 'lxml')
#                 anchor_tags = soup.find_all('a', attrs={"class":"text-default caps searchResultProductName"})
                
#                 for tag in anchor_tags :
#                     med_link = 'https://www.medplusmart.com' + tag.get('href', None)
#                     if med_link not in product_links : product_links.append(med_link)
                    
#                 break 

#         except exceptions.StaleElementReferenceException:  
#             pass
#     print(len(list(set(product_links))),'Links recived from',link.split('/')[-3])
#     print('writing links to file .... ')
#     json.dump({'links':list(set(product_links))},out_file)
#     print('File successfully updated.....')
# #!Remove this break before commit 
#     break 

# out_file.close()
# print('All data saved successfully !!')

print('Getting Medicine data now .....')
links = json.loads(open('medicine_links.json','r' , encoding='ANSI').read())['links']
out_file =  open('medicine_data.json','w+' , encoding='ANSI')


medicine_data = dict()
for link in links :
    try:
                browser.get(link)
                html_text = browser.page_source

    except Exception as err:
                print(str(err))
                break
    else:
                print('\nSuccessfully Accessed:',link)

    soup = None
    if html_text is not None:
            soup = BeautifulSoup(html_text, 'lxml')

    medicine_name = soup.find('h1',attrs={'class':'caps margin-t-none'}).text
    if medicine_name : medicine_data[medicine_name] = dict()
    mfd = browser.find_element_by_xpath("//*[contains(text(), 'Manufacture')]/following-sibling::p/span").text
    if mfd : medicine_data[medicine_name]['Manufacture'] = mfd 
    composition = soup.find('a',attrs={"title":"Click to view relevant composition's products"}).text 
    if composition : medicine_data[medicine_name]['Composition'] = composition
    try :
        form = browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div[1]/div/div[1]/div/div[2]/div/div/div[2]/div/div[1]/div/div[7]/span').text
    except exceptions.NoSuchElementException :
        pass        
    if form : medicine_data[medicine_name]['Form'] = form
    pack_size = browser.find_element_by_xpath("//*[contains(text(), 'Pack Size')]/following-sibling::p/span").text
    if pack_size : medicine_data[medicine_name]['Pack Size'] = pack_size
    price = soup.find('span',attrs={'class':'lead color-red'}).text
    if price : medicine_data[medicine_name]['MRP'] = price 
    if composition is not None or composition != 'Not Available' : 
        composition_parts_num = len(composition.split('+'))
        medicine_data[medicine_name]['Medicine Information'] = dict()
        if composition_parts_num > 1 :
            for i in range(1,composition_parts_num+1) :
                component = soup.find('div', attrs={'id':('tab'+ str(i))})
                headings = component.find_all('h4', attrs={'class':'color-blue'})
                paras = component.find_all('p')
                for heading,para in zip(headings,paras):
                    medicine_data[medicine_name]['Medicine Information'][heading.text]= para.text 
        else : 
            component = soup.find('div', attrs={'id':'tab1'})
            headings = component.find_all('h4', attrs={'class':'color-blue'})
            paras = component.find_all('p')
            for heading,para in zip(headings,paras):
                medicine_data[medicine_name]['Medicine Information'][heading.text]= para.text 
    json.dump(medicine_data,out_file)
    print(medicine_data)

    