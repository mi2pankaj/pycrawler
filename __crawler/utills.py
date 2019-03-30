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
import os
import csv


class GenericMethods():
    
    'contains information about damn pages'
    globalDamnPagesMap = {}
    
    'this map will be used to keep all values'
    globalUrlMap = {}
        
    'this will keep unique urls which are already traversed - to avoid repetition'
    globalTraversedSet = set()
    
    _py_logger = logging.getLogger('GenericMethods')
    
    specificDomain = ''
    regexToParseUrl = ''
    targetURL = ''
    
    ''' this is the main entry method '''
    def entryMethod(self, startURL):
        
        try:            
            
            self.targetURL = startURL
            
#             'get max threads to parse'
#             maxThreads = int(self.get_config_param('crawler', 'max_threads'))
            self.specificDomain = self.get_config_param('crawler', 'specificDomain')
            self.regexToParseUrl = self.get_config_param('crawler', 'regexToParseUrl')
            print('Using regex to parse utl --> '+self.regexToParseUrl)

            self._py_logger.info(f" started crawling with default executor, looking for domain => {self.specificDomain}")         
            self.getInitialUrlsFromSuppliedRequest(startURL)
            
            ''' create an event loop to iterate the global map - async way '''
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)        

            '===> crawl until traversed urls and parsed urls map are not same -- to review ==> not using this thread coz' 
            'if given threads are higher than the allocated work then --> loop is getting broken .. therefore using default executor '
            _executor = concurrent.futures.ThreadPoolExecutor(max_workers=100)
            
#             'synchronous crawling with executor ==> to use this -- remove async and await from all the used methods '
#             loop.run_until_complete(self.start_sync_crawling_with_executor(_executor))
            
            #0. using main thread only -- single threaded 
#             loop.run_until_complete(asyncio.gather(*[self.pick_url_from_global_map()]))
            
            #1. multi-threaded but code not exiting, need to wait for code completion
#             i=1
            _task_list =[]
            while(len(self.globalTraversedSet) < len(self.globalUrlMap)):
                
                url = self.get_url_from_global_map()
                
                if(url != ''):
                    _task = loop.run_in_executor(_executor, self.start_async_crawling_without_executor, url)
                    _task_list.append(_task)
                    
#                     print(i," ==> "+url)
#                     i=i+1
                
            loop.run_until_complete(asyncio.wait(_task_list))
            loop.close()
                                    
            'need to wait until all tasks submitted to executors are completed.. --> need fix here '
#             loop.run_until_complete(asyncio.wait(_task_list))
            
            #2.  using main thread only -- single threaded
#             _task_list = []
#             url = 'none'
#             while(url != ''):
#                 url = self.get_url_from_global_map()
#                 _task = loop.create_task(self.start_async_crawling_without_executor(url))
#                 _task_list.append(_task) 
#             loop.run_until_complete(asyncio.wait(_task_list))
                
#             loop.close()
            
            self._py_logger.info(f' Length of global list after crawling: {len(self.globalTraversedSet)} Length of global DAMN map after crawling: {len(self.globalDamnPagesMap)}')
            self._py_logger.info('********************* Printing Global Damm Map ******************* ')
            self._py_logger.info(self.globalDamnPagesMap)
            
            'write urls in csv'
            with open('BrokenUrls.csv', mode='w') as csv_file:
                writer = csv.writer(csv_file)
                for k,v in self.globalDamnPagesMap.items():                
                    writer.writerow([k,v])
                    #writer.writerow('')
            
        except Exception:
            self._py_logger.error('Exception Occurred: ', exc_info=True)
        
            
    ''' async entry method for crawler '''    
    def start_async_crawling_without_executor(self, url):
        
        ''' create an event loop to iterate the global map - async way '''
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)        
                
        'run a task -- this means execute get_url_from_global_map while itearting the whole globalUrlMap '
#         localMap = self.globalUrlMap
#         loop.run_until_complete(asyncio.gather(*[self.pick_url_from_global_map() for url in localMap]))
        
        'run a task -- means execute get_url_from_global_map method - which browse only one url at a time, here iteration will be controlled by outer loop '
#         loop.run_until_complete(asyncio.gather(*[self.pick_url_from_global_map()]))
        loop.run_until_complete(self.send_http_request_parse_response(url))
        loop.close()


    ''' async entry method for crawler '''    
    def start_sync_crawling_with_executor(self, _executor):
        try:
            loop = asyncio.get_event_loop()
            asyncio.set_event_loop(loop)        
            
            ' using loop with thread pool executor '
            while (len(self.globalTraversedSet) <= len(self.globalUrlMap)):
                loop.run_in_executor(_executor, self.get_url_from_global_map)
                
        except Exception:            
            self._py_logger.error('Exception Occurred: ', exc_info=True)
            

#     ''' async entry method for crawler '''    
#     def start_async_crawling_without_executor(self):
#         
#         ''' create an event loop to iterate the global map - async way '''
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)        
#                 
#         'run a task -- this means execute get_url_from_global_map while itearting the whole globalUrlMap '
# #         localMap = self.globalUrlMap
# #         loop.run_until_complete(asyncio.gather(*[self.pick_url_from_global_map() for url in localMap]))
#         
#         'run a task -- means execute get_url_from_global_map method - which browse only one url at a time, here iteration will be controlled by outer loop '
# #         loop.run_until_complete(asyncio.gather(*[self.pick_url_from_global_map()]))
#         loop.run_until_complete(self.pick_url_from_global_map())
#         
#         loop.close()
    
    
    ''' get config value from configuration '''
    def get_config_param(self, section, key):
        config = configparser.ConfigParser()
        configFile = os.path.dirname(os.path.abspath(__file__))+'/../config/config.ini'
        config.read(configFile)
        self.config = config
        
        print('Using config file - '+configFile)
        return self.config.get(section, key)
  
  
    ''' get domain from received url '''
    def if_desired_domain(self, url):
        url1 = url[url.find('//')+2:]
        url2 = url1[:url1.find('/')]

        if url2.find(self.specificDomain) > -1:
            return True
        else:
            return False
            
    
    ''' get url from global map and browse --> and update further global variable '''   
    async def pick_url_from_global_map(self):
        
        try:
            url = 'none'
            while(url not in ''):
                url = self.get_url_from_global_map()
                await self.send_http_request_parse_response(url)
                
        except Exception:
            self._py_logger.error('Exception Occurred: ', exc_info=True)

                      
    ''' launch crawler through executor using map '''
    def get_url_from_global_map(self):
        
        try:
            lock = threading.RLock()
            lock.acquire(blocking=True)
            
            url = ''
            
            ' storing global map in local variable to avoid exception ==> RuntimeError: dictionary changed size during iteration '
            localUrlMap = self.globalUrlMap
            
            for k,v in list(localUrlMap.items()):
                if(v==False):
                    ' update url to true so that its not picked up again '
                    url = k
                    self.globalUrlMap.update({k:True})
     
                    break
                
        except Exception:
            self._py_logger.error('Exception Occurred While Getting URL From Global Map: ', exc_info=True)
        
        finally:
            lock.release()
            
        return url
            
        
    '''' added a method which return http response - for async handling '''    
    async def get_http_response(self, url):
        return requests.get(url)
        
                
    ''' perform task ==> get url, browse it and check it if its a DAMN and then find the url list and return this '''
#     @asyncio.coroutine
    async def send_http_request_parse_response(self, url):
        
        try:
            url = str(url)
            
            'check only those urls which starts with http and not traversed earlier and having lenskart domain, update them in global map as TRUE so that'
            'not picked up again'
            if((url in self.globalTraversedSet) | (not (self.if_desired_domain(url)))  | (not(url.startswith('http')))):
                try:
                    lock = threading.RLock()
                    lock.acquire(blocking=True)
                    
                    ' update url to true so that its not picked up again '
                    self.globalUrlMap.update({url:True})
                    
                    'handling those condition where url is not of lenskart domain and not starts with http '
                    self.globalTraversedSet.add(url)
                finally:
                    lock.release()

            else:
                'keep a copy so that its not traversed again'
                try:
                    lock = threading.RLock()
                    lock.acquire(blocking=True)
                    self.globalTraversedSet.add(url)
                finally:
                    lock.release() 
                    
                'sending request to received url and parse response and update global urls. '                    
                try:
#                   response = requests.get(url)
                    response = await self.get_http_response(url)
                    pageSource = response.text
                    status_code = response.status_code

                except Exception as e:
                    self._py_logger.error(f' Exception Occurred While Browsing URL: {url} and exception is: {str(e)}')
                    
                    # assigning some value so that in case of exception below status code condition doesn't break coz there will be no status code in exception.
                    pageSource = str(e)
                    status_code = int(777)
                                        
                try:
                    lock = threading.RLock()
                    lock.acquire(blocking=True)
                    
                    if(str(status_code).startswith('4') | str(status_code).startswith('5') | str(status_code).startswith('7')):    
                        self.globalDamnPagesMap.update({url : status_code})
                        self._py_logger.info(f' ERROR == NOT FOUND OR NON RESPONSIVE PAGE  ==> {url} Status_Code ==> {status_code}')
                    
                    # in case of exception while browsing - 
#                     elif(str(status_code).startswith('7')):
#                         self.globalDamnPagesMap.update({url : pageSource})
#                         self._py_logger.info(f' ERROR == BROWSING EXCEPTION PAGE  ==> {url} ')
                    
#                     elif(pageSource.__contains__('DAMN!!')):
#                         self.globalDamnPagesMap.update({url : 'DAMN'})
#                         self._py_logger.info(f' ERROR == DAMN PAGE  ==> {url} Status_Code ==> {status_code}')
                         
                    elif(pageSource.__contains__("This page isn’t working")):
                        self.globalDamnPagesMap.update({url : 777})
                        self._py_logger.info(f' ERROR == NOT WORKING PAGE  ==> {url} Status_Code ==> {status_code}')
                                                                                
                    else:
                        ''' apply regex to get urls from response - urls starting with http '''
                        # urlList = re.findall('(?<=href=").*?(?=")', pageSource)
                        urlList = re.findall(self.regexToParseUrl, pageSource)

                        'add received urls in global map and remove non http urls + already browsed urls + exclude image url.. as they are slow for now ..'
                        for x in urlList:
                            try:
                                x = self.format_url(x)
#                                 self._py_logger.info(f'====> while crawling ==> formatted url ==> {x}')
                                     
                                if ( (x.startswith('http')) & (self.if_desired_domain(x)) 
                                    & ((self.globalUrlMap.get(x) == None) | (self.globalUrlMap.get(x) == False)) 
#                                     & (not (url in self.globalTraversedSet))    #debug condition to use less urls
                                    & (not (x.lower().endswith('.jpg') | x.lower().endswith('.png') | x.lower().endswith('.jpeg'))) ):

                                    self.globalUrlMap.update({x:False})
                                else:
                                    pass
                                                                                
                            except Exception:
                                self._py_logger.error('Exception Occurred: ', exc_info=True)
                    
                except Exception:
                    self._py_logger.error(f' --> Exception Occurred With {url} ', exc_info=True)


                finally:
                    url = url.encode("utf-8")
                    self._py_logger.info(f" global map: {len(self.globalUrlMap)}, traversed: {len(self.globalTraversedSet)}, damn: {len(self.globalDamnPagesMap)}, url ==> {url}, status_code: {status_code}")

                    lock.release()

        except Exception:
            self._py_logger.error('Exception Occurred: ', exc_info=True)


    ''' hit the received request, find the urls from response '''
    def getInitialUrlsFromSuppliedRequest(self, url):
        
        'sending request to received url'                    
        try:
            url = str(url)
            response = requests.get(url)
            pageSource = response.text
            
            ''' apply regex to get urls from response - urls starting with http '''
            # urlList = re.findall('(?<=href=").*?(?=")', pageSource)
            urlList = re.findall(self.regexToParseUrl, pageSource)
                        
            'convert received urls into set for uniqueness and map and remove non http urls + already browsed urls'
            for x in urlList:
                
                x = self.format_url(x)
#                 print('after compilation, url is: '+x)
                
                if ( (x.startswith('http')) & (self.if_desired_domain(x)) & ((self.globalUrlMap.get(x) == None) | (self.globalUrlMap.get(x) == False)) ):
                    self.globalUrlMap.update({x:False})
                else:
                    pass
                                                                                                                                    
        except Exception:
            self._py_logger.error('Exception Occurred: ', exc_info=True)
                
        self._py_logger.info(f' First List Of Received List Of URLs From Supplied Request ===>  {len(self.globalUrlMap)} , Before Manipulation ==> {len(urlList)} ')

        
    ''' format the received url to make it proper '''
    def format_url(self, x):
        
        if( x.startswith('//')):
            x='https:'+x
        elif(x.startswith('/') & (x != '/')):
            x=self.targetURL+x
            
        return x  
    
        

