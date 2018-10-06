'''
Created on 23-Nov-2017

@author: pankaj.katiyar
'''

from selenium import webdriver
import os
import re
from selenium.webdriver.common.by import By
import traceback
import sys
import time
import requests
from __samplemodule import ConfigParser
import threading


class SaareMethods():

    'contains information about damn pages'
    damnPagesMap = {}
    
    'this will be used to keep only unique values'
    globalUrlSet = set()
    
    'this will be used to iterate'
    globalUrlList = []
    
    'this will keep unique urls which are already traversed - to avoid repetition'
    globalTraversedSet = set()
        

    def getDriver(self, whatTypeOfDriver):
        
        try:
        
            if(whatTypeOfDriver == "chrome"):
                
                chromedriver = "/Users/pankaj.katiyar/Desktop/Automation/Lenskart_Automation/tpt/drivers/mac/chromedriver"
                os.environ["webdriver.chrome.driver"] = chromedriver
        
                driver = webdriver.Chrome(chromedriver)
                
                print("Chrome launch ho gaya bhai")
                
            elif(whatTypeOfDriver == "firefox"):
                geckodriver="/Users/pankaj.katiyar/Desktop/Automation/Lenskart_Automation/tpt/drivers/geckodriver/geckodriver"
                os.environ["webdriver.geckodriver.driver"] = geckodriver
        
                driver = webdriver.Firefox()
        
                print("Firefox ho gaya bhai")
            
            else:
                print("Enjoy Maaddi")   
            
        except Exception:
            traceback.print_exc(file=sys.stdout)
            
        return driver
        
    ''' define navigation here like click on Shop and then on Eyeglass or Click on Men and then on Eyeglass etc. '''
    def navigation(self, menuOption, categoryOption):
        try:
            
            xpath = ConfigParser().get_config_param("navigation", menuOption)
            menu_ShopLink = self.driver.find_element(By.XPATH, xpath)
            menu_ShopLink.click()
        
            time.sleep(10)
            
            ''' click on Eyeglasses after clicking on SHOP link '''
            menu_ShopLink_Eyeglasses = self.driver.find_element(By.XPATH, ConfigParser().get_config_param("navigation", categoryOption))
            menu_ShopLink_Eyeglasses.click()
            
            print("Clicked Category link ... "+categoryOption)
            
        except Exception:
            traceback.print_exc(file=sys.stdout)
            
    ''' get all view ranges elements and click on them and then check product images '''
    def getViewRangeHrefList(self):
        
        viewRangeHrefList = []
        try:
            print("Getting all view range objects  ... ")

            ''' find all View Range elements '''
            viewRange = self.driver.find_elements_by_xpath(ConfigParser().get_config_param("generic_locators", "viewRange_Link"))
            
            ''' iterate view range and click on them and then check for product images '''
            for viewrange in viewRange:
                
                ''' add href in a list '''
                viewRangeHrefList.append(viewrange.get_attribute("href"))
                                
        except Exception:
            traceback.print_exc(file=sys.stdout)        
    
        return viewRangeHrefList

    ''' browse href received from View Range object and check for product images '''
    def checkProductImagesOnViewRangeHref(self, hrefList):
                
        print(" received View Range List: "+ str(hrefList.__len__()))
        
        for href in hrefList:
            self.driver.get(href)
            print("Checking product images at: " + href)
            
            self.checkProductImages()
        
    ''' generic method - get product images using generic locator, hit on every url and check for 200 ok '''
    def checkProductImages(self):
        try:
            print("Checking product images ... ")
            productImages = self.driver.find_elements(By.XPATH, ConfigParser().get_config_param("generic_locators", "generic_ProductLocator"))
        
            req = None
            
            ''' iterate each image link and check for 200 ok image url '''
            for productImg in productImages:
                idText = productImg.get_attribute("id")
                srcLink = productImg.get_attribute("src")
                
                ''' send request and get response '''
                req = requests.get(srcLink)
                
                print(idText + "  ---  " + str(req.status_code) + " --- " + srcLink)
            
#             req.close()
        except Exception:
            traceback.print_exc(file=sys.stdout)
            
    ''' return the hrefs '''
    def getLinksFromPage(self, webdriver):
        elementsList = webdriver.find_elements_by_xpath("//a[contains(@href,'http')]");
        
        urlList = []
        for element in elementsList:
            href = element.get_attribute("href")
            urlList.append(href)
            print('Appending ======> '+href)
            
        return urlList
        
    def crawl(self, driver):
        
        urlListMain = self.getLinksFromPage(driver)

        for url in urlListMain:
            if(url.startswith('http')):
                
                try:
                
                    print('Browsing ======> '+url)
                    driver.get(url)
                    
                    urlList = self.getLinksFromPage(driver)
                    
                    print('received main list ==> ', len(urlListMain) , '#### found new urls ==> ', len(urlList))
                    
                    urlListMain.extend(urlList)
                    
                    print('#### grown size ==> ', len(urlListMain))
                    
                    urlListMain.remove(url)
                    
                    print('#### after remving url size is ==> ', len(urlListMain))
                    
                except Exception:
                    traceback.print_exc(file=sys.stdout);
                
        print('######### it ends here #########')

    ''' perform task ==> get url, browse it and check it if its a DAMN and then find the url list and return this '''
    def performTaskWithBrowser(self, driver, url):
        
        if(url.startswith('http')):
            
            print('browsing url ==> '+url)
            driver.get(url)
            
            'get page source'
            pageSource = driver.page_source
                        
            if(pageSource.__contains__('DAMN!!') | pageSource.__contains__('This page isn’t working')):
                
                print('Found a DAMN Page  ==> '+url)
                self.damnPagesMap.update({url : "damn page"})
                
            'now get the url list from the received url'
            urlListFromPage = self.getLinksFromPage(driver)
            print('received number of urls ==> ', len(urlListFromPage))
            
            'update the global url list'
            self.globalUrlSet.extend(urlListFromPage)
            
            'remove the browsed url'
            self.globalUrlSet.remove(url)
            
            print('global list increased to ==> ', len(self.globalUrlSet), ' DAMN map increased to ' , len(self.damnPagesMap))
        
        else:
            print('not browsing url: ==> '+url)


    ''' get domain from received url '''
    def ifLenskartDomain(self, url):
        url1 = url[url.find('//')+2:]
        url2 = url1[:url1.find('/')]
        
#         print('domain: '+url2 + ' from received url: '+url)
        
        if url2.find('lenskart') > -1:
            return True
        else:
            return False
        
        
    ''' launch crawler through executor '''
    def launchCrawler(self):
        
        while len(self.globalUrlList) > 0:
            for url in self.globalUrlList:
                 
                try:
                    self.performTaskWithoutBrowser(url)
                     
                except Exception:
                    print('error ---> ')
     
        
    ''' perform task ==> get url, browse it and check it if its a DAMN and then find the url list and return this '''
    def performTaskWithoutBrowser(self, url):
        
        try:
            url = str(url)
            
            lock = threading.RLock()
            lock.acquire(blocking=True)
            
            try: 
                if url in self.globalUrlSet:
                    self.globalUrlSet.remove(url)
                    
                'update the global list with unique values of set '
                self.globalUrlList = list(self.globalUrlSet)
            finally:
                lock.release()
            
            'check only those urls which starts with http and not traversed earlier and having lenskart domain'
            if(url in self.globalTraversedSet):
                print('')
               
            elif not (self.ifLenskartDomain(url)):
                print('')
                  
            elif not(url.startswith('http')):
                print('')
                    
            else:
                flag = True
                try:
                    'keep a copy so that its not traversed again'
                    lock = threading.RLock()
                    lock.acquire(blocking=True)
                    try:
                        self.globalTraversedSet.add(url)
                    finally:
                        lock.release() 
                    
                    print('browsing url, before browsing, appending http -- ==> ' +url)
                    response = requests.get(url)
                    
                except Exception:
                    flag = False
                    print('exception occurred with url ==> ' +url)
                
                print('browsed url ==> ' +url + " *************** flag - ", flag)
                
                if(flag):
                    pageSource = response.text
                    status_code = response.status_code
                    
                    print('status_code ====> ', status_code, '  url ===> '+url)
                                
                    if(str(status_code).startswith('4') | str(status_code).startswith('5')):
                        
                        print('Found a non responsive page  ==> '+url + " status code ==> ", status_code)
                        
                        lock = threading.RLock()
                        lock.acquire(blocking=True)
                        try:            
                            self.damnPagesMap.update({url : status_code})
                        finally:
                            lock.release()
                            
                    elif(pageSource.__contains__('DAMN!!') | pageSource.__contains__('This page isn’t working')):
                        
                        print('Found a DAMN Page  ==> '+url)
                            
                        lock = threading.RLock()
                        lock.acquire(blocking=True)
                        try:            
                            self.damnPagesMap.update({url : 'DAMN'})
                        finally:
                            lock.release()
                                                    
                    else:
                        ''' apply regex to get urls from response - urls starting with http '''
                        urlList = re.findall('(?<=href=").*?(?=")', pageSource)

                        'convert into set and remove non http urls '
                        for x in urlList:
                            if ( (not(x.startswith('http'))) & (not(self.ifLenskartDomain(url)))):
                                urlList.remove(x)
                                
                        s = set(urlList)                            
                        print('received number of urls ==> ', len(urlList) , " and global set ==> ", len(self.globalUrlSet))
                        
                        ''' update the global url set and list '''
                        lock = threading.RLock()
                        lock.acquire(blocking=True)
                        try:
                            print(' ====>====>====> Before Updating  - Global Set: ', len(self.globalUrlSet))
                            self.globalUrlSet.update(s)
                            print(' ====>====>====> After Updating  - Global Set: ', len(self.globalUrlSet))
                                                       
                            'update the global list with unique values of set '
                            self.globalUrlList = list(self.globalUrlSet)
 
                            print('received urls from browsing ==> ', len(s), ' extended global set to ==> ', len(self.globalUrlSet) , ' extended global list to ==> ', len(self.globalUrlList))
                        except Exception:
                            traceback.print_exc(file=sys.stdout)
                            
                        finally:
                            lock.release()

                    
            print('end of thread: global traversed set ==> ',len(self.globalTraversedSet), 'global set ==> ', len(self.globalUrlSet), ' global list ==> ', len(self.globalUrlList) ,' global DAMN map ==> ' , len(self.damnPagesMap), ' ==> url ==> '+url)

        except Exception:
            traceback.print_exc(file=sys.stdout)


