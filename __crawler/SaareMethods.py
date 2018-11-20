'''
Created on 23-Nov-2017

@author: pankaj.katiyar
'''

import re
import traceback
import sys
import requests
import threading
import configparser
import concurrent.futures
import time
from datetime import datetime

import asyncio

class SaareMethods():

    'contains information about damn pages'
    globalDamnPagesMap = {}
    
    'this map will be used to keep all values'
    globalUrlMap = {}
        
    'this will keep unique urls which are already traversed - to avoid repetition'
    globalTraversedSet = set()
        
    globalTaskList =[]
        
    ''' this is the main entry method '''
    def entryMethod(self, startURL):
        
        try:        
            'get max threads to parse'
            maxThreads = int(self.get_config_param('crawler', 'max_threads'))
        
            print('started crawling with max threads ==> ', maxThreads)         
            self.getInitialUrlsFromSuppliedRequest(startURL)
            
            ''' create an event loop to iterate the global map - async way '''
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)        

            '===> crawl until traversed urls and parsed urls map are not same -- to review ==> '
            _executor = concurrent.futures.ThreadPoolExecutor(max_workers=maxThreads)
            
            'synchronous crawling with executor ==> to use this -- remove async and await from all the used methods '
#             loop.run_until_complete(self.synchronous_crawling_using_executor(_executor))
            
            while (len(self.globalTraversedSet) < len(self.globalUrlMap)):
#                 loop.run_in_executor(_executor, self.crawlUsingMap)
                loop.run_in_executor(_executor,self.async_crawling)
                
            loop.run_until_complete(self.async_crawling)
            loop.close()
            
            print()
            print('Length of global list after crawling ==> ', len(self.globalTraversedSet) , ' Length of global DAMN map after crawling ' , len(self.globalDamnPagesMap))
    
            print(self.globalDamnPagesMap)
    
        except Exception:
            traceback.print_exc(file=sys.stdout)
    

    ''' async entry method for crawler '''    
    def synchronous_crawling_using_executor(self, _executor):
        try:
            loop = asyncio.get_event_loop()
            
            ' using loop with thread pool executor '
            while (len(self.globalTraversedSet) <= len(self.globalUrlMap)):
                loop.run_in_executor(_executor, self.crawlUsingMap)
                
        except Exception:            
            traceback.print_exc(file=sys.stdout)
            

    ''' async entry method for crawler '''    
    def async_crawling(self):
        
        ''' create an event loop to iterate the global map - async way '''
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)        
                
        'run a task -- this means execute crawlUsingMap while itearting the whole globalUrlMap '
#         localMap = self.globalUrlMap
#         loop.run_until_complete(asyncio.gather(*[self.crawlUsingMap() for url in list(localMap)]))
        
        'run a task -- means execute crawlUsingMap method - which browse only one url at a time, here iteration will be controlled by outer loop '
        loop.run_until_complete(asyncio.gather(*[self.crawlUsingMap()]))
        
        loop.close()
    
    
    ''' get config value from configuration '''
    def get_config_param(self, section, key):
        config = configparser.ConfigParser()
        config.read("/Users/pankaj.katiyar/Desktop/Automation/PythonCrawler/config/config.ini")
        self.config = config

        return self.config.get(section, key)
  
  
    ''' get domain from received url '''
    def ifLenskartDomain(self, url):
        url1 = url[url.find('//')+2:]
        url2 = url1[:url1.find('/')]
        
#         print('domain: '+url2 + ' from received url: '+url)
        
        if url2.find('lenskart') > -1:
            return True
        else:
            return False
        
        
    ''' launch crawler through executor using list '''
    async def crawlUsingList(self):
#         while len(self.globalUrlList) > 0:   
        
        'global list will be updated dynamically by many threads '
        tempList = self.globalUrlList     
        
        print(' =======  iteration list is now  ==> ', len(tempList))
           
        for url in tempList:
            try:
                self.performTaskWithoutBrowser(url)
            except Exception:
                print('error ---> ')
            
            
    ''' launch crawler through executor using map '''
    async def crawlUsingMap(self):
        
        try:
            url = ''
            for k,v in self.globalUrlMap.items():
                if(v==False):
                    try:
                        lock = threading.RLock()
                        lock.acquire(blocking=True)
                         
                        ' update url to true so that its not picked up again '
                        url = k
                        self.globalUrlMap.update({k:True})
                        
                        print()
                        print("Time: "+datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') +" Thread: ", format(threading.current_thread()), 'global map: ', len(self.globalUrlMap), ' url is ==> '+url)
                        await self.performTaskWithoutBrowser(url)
     
                    finally:
                        lock.release()
                                    
                    break
        except Exception:
            traceback.print_exc(file=sys.stdout)
            
            
        
    '''' added a method which return http response - for async handling '''    
    async def get_http_response(self, url):
        try:
            return requests.get(url)
        except Exception:
            traceback.print_exc(file=sys.stdout)
        
        
    ''' perform task ==> get url, browse it and check it if its a DAMN and then find the url list and return this '''
#     @asyncio.coroutine
    async def performTaskWithoutBrowser(self, url):
        
        try:
            url = str(url)
 
            'check only those urls which starts with http and not traversed earlier and having lenskart domain, update them in global map as TRUE so that'
            'not picked up again'
            if((url in self.globalTraversedSet) | (not (self.ifLenskartDomain(url)))  | (not(url.startswith('http')))):
                
                try:
                    lock = threading.RLock()
                    lock.acquire(blocking=True)
                    
                    ' update url to true so that its not picked up again '
                    self.globalUrlMap.update({url:True})
                finally:
                    lock.release()

            else:
                try:
                    'keep a copy so that its not traversed again'
                    lock = threading.RLock()
                    lock.acquire(blocking=True)
                    try:
                        self.globalTraversedSet.add(url)
                    finally:
                        lock.release() 
                    
                    'sending request to received url'                    
                    try:
#                         response = requests.get(url)
                        response = await self.get_http_response(url)
                        pageSource = response.text
                        status_code = response.status_code

                    except Exception:
#                         traceback.print_exc(file=sys.stdout)
                        pageSource = 'This page isn’t working'
                        status_code = int(200)
                    
                    print(' ^^^^^^^^^^^^^^^^^ status_code ====> ', status_code, '  url ===> '+url )
                                
                    if(str(status_code).startswith('4') | str(status_code).startswith('5')):
                        
                        print('Found a non responsive page  ==> '+url + " status code ==> ", status_code)
                        
                        lock = threading.RLock()
                        lock.acquire(blocking=True)
                        try:            
                            self.globalDamnPagesMap.update({url : status_code})
                        finally:
                            lock.release()
                            
                    elif(pageSource.__contains__('DAMN!!')):
                        print('Found a DAMN Page  ==> '+url)
                            
                        lock = threading.RLock()
                        lock.acquire(blocking=True)
                        try:            
                            self.globalDamnPagesMap.update({url : 'DAMN'})
                        finally:
                            lock.release()
                    
                    elif(pageSource.__contains__("This page isn’t working")):
                        print("This page isn't working ==> "+url)
                             
                        lock = threading.RLock()
                        lock.acquire(blocking=True)
                        try:            
                            self.globalDamnPagesMap.update({url : 'Not_Working_Page'})
                        finally:
                            lock.release()
                                                    
                    else:
                        ''' apply regex to get urls from response - urls starting with http '''
                        urlList = re.findall('(?<=href=").*?(?=")', pageSource)
                        
                        ''' update the global url set and list '''
                        lock = threading.RLock()
                        lock.acquire(blocking=True)
                        try:
                            'convert received urls into set for uniqueness and map and remove non http urls + already browsed urls'
                            for x in urlList:
                                if ( (x.startswith('http')) & (self.ifLenskartDomain(x)) & ((self.globalUrlMap.get(x) == None) | (self.globalUrlMap.get(x) == False)) ):
                                    self.globalUrlMap.update({x:False})
                                else:
                                    urlList.remove(x)

                            print('After Updating, traversed ==> ',len(self.globalTraversedSet), ' global map ==> ', len(self.globalUrlMap), ' global damn map ==> ' , len(self.globalDamnPagesMap))
                                                    
                        except Exception:
                            traceback.print_exc(file=sys.stdout)
                            
                        finally:
                            lock.release()
                            
                except Exception:
                    print('exception occurred with url ==> ' +url)
                    traceback.print_exc(file=sys.stdout)
                    
#             print('final global traversed set ==> ',len(self.globalTraversedSet), ' global map ==> ', len(self.globalUrlMap), ' global DAMN map ==> ' , len(self.globalDamnPagesMap))
            
        except Exception:
            traceback.print_exc(file=sys.stdout)



    ''' hit the received request, find the urls from response '''
    def getInitialUrlsFromSuppliedRequest(self, url):
        
        'sending request to received url'                    
        try:
            url = str(url)
            response = requests.get(url)
            pageSource = response.text
            
            ''' apply regex to get urls from response - urls starting with http '''
            urlList = re.findall('(?<=href=").*?(?=")', pageSource)
                        
            'convert received urls into set for uniqueness and map and remove non http urls + already browsed urls'
            for x in urlList:
                if ( (x.startswith('http')) & (self.ifLenskartDomain(x)) & ((self.globalUrlMap.get(x) == None) | (self.globalUrlMap.get(x) == False)) ):
                    self.globalUrlMap.update({x:False})
                else:
                    urlList.remove(x)
                                                                                                                    
        except Exception:
            traceback.print_exc(file=sys.stdout)
            
        print(' First List Of Received List Of URLs From Supplied Request ===> ', len(self.globalUrlMap))



