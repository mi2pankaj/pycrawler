'''
Created on 24-Nov-2017

@author: pankaj.katiyar

in any class return variable with self and in other class, create the instance of first class and then use the returned values like:
    saareMethodObject = SaareMethods.SaareMethods()        
    saareMethodObject.getDriver("chrome")
    driver = saareMethodObject.driver
'''
from __crawler import SaareMethods
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
        startURL = 'https://lenskart.com?s=1111'
        
        'create object of class'
        saareMethodObject = SaareMethods.SaareMethods()
        
        'get max threads to parse'
        maxThreads = int(saareMethodObject.get_config_param('crawler', 'max_threads'))
        
        print('started crawling with max threads ==> ', maxThreads)         
        saareMethodObject.performTaskWithoutBrowser(startURL)
        
        ' ===> crawl until traversed urls and parsed urls map are not same -- to review ==> '
        with ThreadPoolExecutor(max_workers=maxThreads) as executor:
            while (len(saareMethodObject.globalDamnPagesMap) < len(saareMethodObject.globalUrlMap)):
                executor.submit(saareMethodObject.launchCrawlerUsingMap)                
        
        print()
        print('Length of global list after crawling ==> ', len(saareMethodObject.globalTraversedSet) , ' Length of global DAMN map after crawling ' , len(saareMethodObject.damnPagesMap))

    except Exception as err:
        traceback.print_exc(file=sys.stdout)
    
    st2 = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print('end time ==> '+st2 + ' start time ==> '+st1 + ' ===> dammn map ===> ',saareMethodObject.globalDamnPagesMap)
    
    print(saareMethodObject.damnPagesMap)
    
    
    
    
    