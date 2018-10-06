'''
Created on 24-Nov-2017

@author: pankaj.katiyar

in any class return variable with self and in other class, create the instance of first class and then use the returned values like:
    saareMethodObject = SaareMethods.SaareMethods()        
    saareMethodObject.getDriver("chrome")
    driver = saareMethodObject.driver
'''
from __samplemodule.BrowserCrawling import SaareMethods
from concurrent.futures.thread import ThreadPoolExecutor

'''
use regex to (?<=href=").*?(?=") to find out the url in response and add them in a list if starts with http
'''

import traceback
import sys
import time
from datetime import datetime


if __name__ == '__main__':
    
    try:
        st1 = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        
        #startURL = 'http://wepaste.com/'    
        #startURL = 'http://www.tutorialspoint.com/python/python_multithreading.htm'
        startURL = 'https://lenskart.com'
        
        ''' create object of class '''
        saareMethodObject = SaareMethods.SaareMethods()            
        saareMethodObject.globalUrlList.append(startURL)
        
        print('started crawling ---> ') 
        saareMethodObject.performTaskWithoutBrowser(startURL)
         
        with ThreadPoolExecutor(max_workers=150) as executor:
         
            while len(saareMethodObject.globalUrlList) > 0:
                executor.submit(saareMethodObject.launchCrawler, )
        
#         while len(saareMethodObject.globalUrlList) > 0:
#             for url in saareMethodObject.globalUrlList:
#                 
#                 try:
# #                     saareMethodObject.performTaskWithoutBrowser(url)
#                     executor.submit(saareMethodObject.performTaskWithoutBrowser, (url,))
#                     
#                 except Exception:
#                     print('error ---> ')
        
        
        print('Length of global list after crawling ==> ', len(saareMethodObject.globalUrlList) , ' Length of global DAMN map after crawling ' , len(saareMethodObject.damnPagesMap))

    except Exception as err:
        traceback.print_exc(file=sys.stdout)
    
    st2 = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print('end time ==> '+st2 + ' start time ==> '+st1 + ' ===> dammn map ===> ', )
    
    print(saareMethodObject.damnPagesMap)
    
    
    
    
    