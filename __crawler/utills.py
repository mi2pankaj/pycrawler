'''
Created on 23-Nov-2017

@author: pankaj.katiyar
'''

import re
import requests
import threading
import configparser
import concurrent.futures
import asyncio
import logging
from __crawler_logging_module.crawler_logging import __py_logger


class GenericMethods():

    'contains information about damn pages'
    globalDamnPagesMap = {}
    
    'this map will be used to keep all values'
    globalUrlMap = {}
        
    'this will keep unique urls which are already traversed - to avoid repetition'
    globalTraversedSet = set()
        
    globalTaskList =[]
    
    __py_logger = logging.getLogger('GenericMethods')
    
    specificDomain =''
    
    ''' this is the main entry method '''
    def entryMethod(self, startURL):
        
        try:            
            
            'get max threads to parse'
            maxThreads = int(self.get_config_param('crawler', 'max_threads'))
            self.specificDomain = self.get_config_param('crawler', 'specificDomain')
            
            self.__py_logger.info(f' started crawling with max threads ==> {str(maxThreads)}  ==> looking for domain => {self.specificDomain} ')         
            self.getInitialUrlsFromSuppliedRequest(startURL)
            
            ''' create an event loop to iterate the global map - async way '''
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)        

            '===> crawl until traversed urls and parsed urls map are not same -- to review ==> '
            _executor = concurrent.futures.ThreadPoolExecutor(max_workers=maxThreads)
            
#             'synchronous crawling with executor ==> to use this -- remove async and await from all the used methods '
#             loop.run_until_complete(self.start_sync_crawling_with_executor(_executor))
            
            '===> running code in async way '
            while (len(self.globalTraversedSet) != len(self.globalUrlMap)):
                loop.run_in_executor(None, self.start_async_crawling_without_executor)

            loop.run_until_complete(self.start_async_crawling_without_executor)                

            loop.close()
            
            self.__py_logger.info('Length of global list after crawling ==> ', len(self.globalTraversedSet) , ' Length of global DAMN map after crawling ' , len(self.globalDamnPagesMap))
            self.__py_logger.info(self.globalDamnPagesMap)
    
        except Exception:
            self.__py_logger.error('Exception Occurred: ', exc_info=True)
    

    ''' async entry method for crawler '''    
    def start_sync_crawling_with_executor(self, _executor):
        try:
            loop = asyncio.get_event_loop()
            
            ' using loop with thread pool executor '
            while (len(self.globalTraversedSet) <= len(self.globalUrlMap)):
                loop.run_in_executor(_executor, self.get_url_from_map)
                
        except Exception:            
            self.__py_logger.error('Exception Occurred: ', exc_info=True)
            

    ''' async entry method for crawler '''    
    def start_async_crawling_without_executor(self):
        
        ''' create an event loop to iterate the global map - async way '''
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)        
                
        'run a task -- this means execute get_url_from_map while itearting the whole globalUrlMap '
#         localMap = self.globalUrlMap
#         loop.run_until_complete(asyncio.gather(*[self.pick_url_from_global_map() for url in localMap]))
        
        'run a task -- means execute get_url_from_map method - which browse only one url at a time, here iteration will be controlled by outer loop '
#         loop.run_until_complete(asyncio.gather(*[self.pick_url_from_global_map()]))
        loop.run_until_complete(self.pick_url_from_global_map())
        
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
        
#         self.__py_logger.info('domain: '+url2 + ' from received url: '+url)
        
        if url2.find(self.specificDomain) > -1:
            return True
        else:
            return False
        
        
    ''' launch crawler through executor using list '''
    async def crawlUsingList(self):
#         while len(self.globalUrlList) > 0:   
        
        'global list will be updated dynamically by many threads '
        tempList = self.globalUrlList     
        
        self.__py_logger.info(' =======  iteration list is now  ==> ', len(tempList))
           
        for url in tempList:
            try:
                self.send_http_request_parse_response(url)
            except Exception:
                self.__py_logger.error('Exception: ', exc_info=True)
            
    
    ''' get url from global map and browse --> and update further global variable '''   
    async def pick_url_from_global_map(self):
        
        try:
            url = self.get_url_from_map()
            await self.send_http_request_parse_response(url)
        except Exception:
            self.__py_logger.error('Exception Occurred: ', exc_info=True)
                  
            
    ''' launch crawler through executor using map '''
    def get_url_from_map(self):
        
        try:
            url = ''
            ' storing global map in local variable to avoid exception ==> RuntimeError: dictionary changed size during iteration '
            localUrlMap = self.globalUrlMap
            
            for k,v in localUrlMap.items():
                if(v==False):
                    try:
                        lock = threading.RLock()
                        lock.acquire(blocking=True)
                         
                        ' update url to true so that its not picked up again '
                        url = k
                        self.globalUrlMap.update({k:True})
     
                    finally:
                        lock.release()
                        break
                    
        except Exception:
            self.__py_logger.error('Exception Occurred: ', exc_info=True)
        
        return url
            
        
    '''' added a method which return http response - for async handling '''    
    async def get_http_response(self, url):
        try:
            response = requests.get(url)
            return response  
        except Exception as e:
            self.__py_logger.error(f' Exception Occurred While Getting Response From URL: {url}', exc_info=True)
            # assigning some value so that in case of exception below status code condition doesn't break coz there will be no status code in exception.
            response.pageSource = 'Exception_While_Browsing_URL'
            response.status_code = int(777)
            try:      
                lock = threading.RLock()
                lock.acquire(blocking=True)      
                self.globalDamnPagesMap.update({url : str(e)})
                __py_logger.info(f' {url} is updated in damm map. ')
            finally:
                lock.release()      
        
        
    ''' perform task ==> get url, browse it and check it if its a DAMN and then find the url list and return this '''
#     @asyncio.coroutine
    async def send_http_request_parse_response(self, url):
        
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
                    try:
                        lock = threading.RLock()
                        lock.acquire(blocking=True)
                        self.globalTraversedSet.add(url)
                    finally:
                        lock.release() 
                    
                    'sending request to received url'                    
                    try:
#                         response = requests.get(url)
                        response = await self.get_http_response(url)
                        pageSource = response.text
                        status_code = response.status_code

                    except Exception as e:
                        self.__py_logger.error(f' Exception Occurred While Browsing URL: {url}', exc_info=True)
                        pageSource = 'Exception_While_Browsing_URL'
                        # assigning some value so that in case of exception below status code condition doesn't break coz there will be no status code in exception.
                        status_code = int(777)
                        
                        try:      
                            lock = threading.RLock()
                            lock.acquire(blocking=True)      
                            self.globalDamnPagesMap.update({url : str(e)})
                        finally:
                            lock.release()
                                                    
                    if(str(status_code).startswith('4') | str(status_code).startswith('5')):
                        
                        self.__py_logger.info(f' Found a non responsive page  ==> {url} with status code ==> {status_code}')
                        
                        try:
                            lock = threading.RLock()
                            lock.acquire(blocking=True)        
                            self.globalDamnPagesMap.update({url : status_code})
                        finally:
                            lock.release()
                    
                    # in case of exception - don't do anything - already handled while browsing.
                    elif(pageSource.__contains__('Exception_While_Browsing_URL')):
                        pass
                    
                    elif(pageSource.__contains__('DAMN!!')):
                        self.__py_logger.info('Found a DAMN Page  ==> '+url)

                        try:    
                            lock = threading.RLock()
                            lock.acquire(blocking=True)        
                            self.globalDamnPagesMap.update({url : 'DAMN'})
                        finally:
                            lock.release()
                    
                    elif(pageSource.__contains__("This page isn’t working")):
                        self.__py_logger.info("This page isn't working ==> "+url)
                             
                        try:      
                            lock = threading.RLock()
                            lock.acquire(blocking=True)      
                            self.globalDamnPagesMap.update({url : 'Not_Working_Page'})
                        finally:
                            lock.release()
                                                    
                    else:
                        ''' apply regex to get urls from response - urls starting with http '''
                        urlList = re.findall('(?<=href=").*?(?=")', pageSource)
                        
                        ''' update the global url set and list '''
                        try:
                            lock = threading.RLock()
                            lock.acquire(blocking=True)
                        
                            'convert received urls into set for uniqueness and map and remove non http urls + already browsed urls'
                            for x in urlList:
                                if ( (x.startswith('http')) & (self.ifLenskartDomain(x)) & ((self.globalUrlMap.get(x) == None) | (self.globalUrlMap.get(x) == False)) ):
                                    self.globalUrlMap.update({x:False})
                                else:
                                    urlList.remove(x)
#                             '%Y-%m-%d %H:%M:%S'
                            self.__py_logger.info(f" global map: {len(self.globalUrlMap)}, traversed: {len(self.globalTraversedSet)}, damn: {len(self.globalDamnPagesMap)}, url ==> {url}")
                                                                                
                        except Exception:
                            self.__py_logger.error('Exception Occurred: ', exc_info=True)
                            
                        finally:
                            lock.release()
                            
                except Exception:
                    self.__py_logger.error(f'Exception Occurred With {url} ', exc_info=True)
                    
#             self.__py_logger.info('final global traversed set ==> ',len(self.globalTraversedSet), ' global map ==> ', len(self.globalUrlMap), ' global DAMN map ==> ' , len(self.globalDamnPagesMap))
            
        except Exception:
            self.__py_logger.error('Exception Occurred: ', exc_info=True)



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
            self.__py_logger.error('Exception Occurred: ', exc_info=True)
            
        self.__py_logger.info(f' First List Of Received List Of URLs From Supplied Request ===>  {len(self.globalUrlMap)}')



