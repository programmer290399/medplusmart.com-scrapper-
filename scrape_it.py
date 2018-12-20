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
import re



browser = None

try:
    browser = webdriver.Chrome()
except Exception as error:
    print(error)
# here we get the links of all the categories 
bar = IncrementalBar('Fetching Categories :',max = 2)

out_file = open('category_links.json','w+' , encoding='ANSI')

link_treasure_box = ['https://www.medplusmart.com/pharmaHome#DrugsbyTherapeutic','https://www.medplusmart.com/pharmaHome#surgicalProduct']

links = list()

i = 0 
for link in  link_treasure_box :
    try:
                browser.get(link)
                

    except Exception as err:
                print(str(err))
                break
    else:
                print('\nSuccessfully Accessed:',link)


    if i == 0 : category_heads = browser.find_element_by_xpath('//div[@id="DrugsbyTherapeutic"]').find_elements_by_xpath('//ul[@class="drugsCategory"]') ; i+=1
    #soup.find('div',attrs={'id':"DrugsbyTherapeutic"}).find('ul', attrs={'class':"drugsCategory"}) ; i+=1 
    else :  category_heads = browser.find_element_by_xpath('//div[@id="surgicalProduct"]').find_elements_by_xpath('//ul[@class="drugsCategory"]') 
    # soup.find('div',attrs={'id':"surgicalProduct"}).find('ul', attrs={'class':"drugsCategory"})
    anchor_tags = map(lambda tag: tag.find_elements_by_tag_name('a'),category_heads)
    for tag_bag in anchor_tags :
        for tag in tag_bag :
            links.append(tag.get_attribute("href"))
    bar.next()
        
bar.finish()
print('\n',len(links),'Links Recieved')


print('Writing to file ....')
json.dump({'links': list(set(links))},out_file)
out_file.close()
print('File successfully saved !!')

# Here we scrap the links of every single product from their respective category pages 
links = json.loads(open('category_links.json','r' , encoding='ANSI').read())['links']
out_file = open('medicine_links.json','w+' , encoding='ANSI')

product_links = list()
print('Fetching Medicines by category now ....')

for link in links :
    print('Working on :' ,link.split('/')[-3])
    try:
                browser.get(link)
                

    except Exception as err:
                print(str(err))
                break
    else:
                print('Successfully Accessed:',link)
                print('Please be patient it may take several minutes .....')

    
    
    while True :
        try :
             element = browser.find_element_by_xpath('//*[@id="pagination"]/ul/li[8]/a')
        except NoSuchElementException:
            time.sleep(1)
            
            anchor_tags = browser.find_elements_by_xpath('//a[@class="text-default caps searchResultProductName"]') 
            # soup.find_all('a', attrs={"class":"text-default caps searchResultProductName"})
                
            for tag in anchor_tags :
                product_links.append(tag.get_attribute("href"))
                    
            break 
        time.sleep(1)
        element = WebDriverWait(browser, 120 ,ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,))\
                        .until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '#pagination > ul > li:nth-child(8) > a')))
        try :
            if element.get_attribute("onclick") :
                time.sleep(1)
                anchor_tags = browser.find_elements_by_xpath('//a[@class="text-default caps searchResultProductName"]') 
                # soup.find_all('a', attrs={"class":"text-default caps searchResultProductName"})
                
                for tag in anchor_tags :
                    product_links.append(tag.get_attribute("href"))
                
                browser.execute_script("arguments[0].click();", element)
                time.sleep(1)
            else :
                time.sleep(1)
                anchor_tags = browser.find_elements_by_xpath('//a[@class="text-default caps searchResultProductName"]') 
            # soup.find_all('a', attrs={"class":"text-default caps searchResultProductName"})
                
                for tag in anchor_tags :
                    product_links.append(tag.get_attribute("href"))
                
                break 

        except exceptions.StaleElementReferenceException:  
            pass
    
    print('writing links to file .... ')
    out_file.seek(0)
    out_file.truncate()
    json.dump({'links':list(set(product_links))},out_file)
    print('File successfully updated.....')


out_file.close()
print('All data saved successfully !!')

# Here we scrap medicine data 

print('Getting Medicine data now .....')
links = json.loads(open('medicine_links.json','r' , encoding='ANSI').read())['links']
out_file =  open('medicine_data.json','w+' , encoding='ANSI')


medicine_data = dict()
for link in links :
    try:
            browser.get(link)
            # html_text = browser.page_source

    except Exception as err:
            print(str(err))
            break
    else:
            print('\nSuccessfully Accessed:',link)

    try :
        medicine_name = browser.find_element_by_xpath('//h1[@class="caps margin-t-none"]').text 
        #soup.find('h1',attrs={'class':'caps margin-t-none'}).text
        medicine_data[medicine_name] = dict()
    except NoSuchElementException :
        continue
    try :
        mfd = browser.find_element_by_xpath('//div[text()="Manufacture"][@class="col-xs-4 col-sm-3 col-md-3 padding-none color-label"]//following-sibling::div/child::span').text
        #soup.find(lambda tag : tag.name == 'div' and tag.text == 'Manufacture', attrs={'class':'col-xs-4 col-sm-3 col-md-3 padding-none color-label'})
        medicine_data[medicine_name]['Manufacture'] = re.sub('\s+', '', mfd) #mfd.findNextSibling('div').findChild('span').text
    except NoSuchElementException :
        pass    
    try :
        composition = browser.find_element_by_xpath('//a[@title="{}"]'.format("Click to view relevant composition's products")).text  
        #soup.find('a',attrs={"title":"Click to view relevant composition's products"}).text 
        medicine_data[medicine_name]['Composition'] = composition
    except NoSuchElementException :
        pass    
    try :
        form = browser.find_element_by_xpath('//div[text()="Form"][@class="col-xs-4 col-sm-3 col-md-3 padding-none color-label"]//following-sibling::div/child::span').text
        medicine_data[medicine_name]['Form'] = form
    except exceptions.NoSuchElementException :
        pass         
    try :
        pack_size = browser.find_element_by_xpath('//div[text()="Pack Size"][@class="col-xs-4 col-sm-3 col-md-3 padding-none color-label"]//following-sibling::div/child::span').text 
        # soup.find(lambda tag : tag.name == 'div' and tag.text == 'Pack Size' , attrs={'class':'col-xs-4 col-sm-3 col-md-3 padding-none color-label'})
        medicine_data[medicine_name]['Pack Size'] = re.sub('\s+', '', pack_size) #pack_size.findNextSibling('div').findChild('span').text
    except NoSuchElementException :
        pass    
    try :
        price = browser.find_element_by_xpath('//span[@class="lead color-red"]')
        # soup.find('span',attrs={'class':'lead color-red'})
        medicine_data[medicine_name]['MRP'] = price.text 
    except NoSuchElementException :
        pass
        
    if composition is not None or composition != 'Not Available' : 
        # composition_parts_num = len(composition.split('+'))
        medicine_data[medicine_name]['Medicine Information'] = dict()
        # if composition_parts_num > 1 :
        #     for i in range(1,composition_parts_num+1) :
        try :
                    # component = browser.find_element_by_xpath('//div[@id="{}"]'.format('tab'+str(i))) 
                    # soup.find('div', attrs={'id':('tab'+ str(i))})
                    headings = browser.find_elements_by_xpath('//div[@class="tabbable"]//child::h4') 
                    print(len(list(map(lambda heading: heading.text,headings))))
                    # component.find_all('h4', attrs={'class':'color-blue'})
                    paras = browser.find_elements_by_xpath('//div[@class="row-fluid margin-l-r-20-m"]//child::p')
                    print(len(list(map(lambda heading : heading.text,paras))))
                    # component.find_all('p')
                    for heading,para in zip(headings,paras):
                        medicine_data[medicine_name]['Medicine Information'][heading.get_attribute('textContent')]= para.get_attribute('textContent') 
        except NoSuchElementException:
                    continue
    
    
    print('Writing to file')
    out_file.seek(0)
    out_file.truncate()
    json.dump(medicine_data,out_file)

out_file.seek(0)
out_file.truncate()
json.dump(medicine_data,out_file)
print('All data scrapped Successfullly !!!')
out_file.close()
browser.close()
    
