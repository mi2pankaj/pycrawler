'''
Created on 24-Nov-2017

@author: pankaj.katiyar

in any class return variable with self and in other class, create the instance of first class and then use the returned values like:
    saareMethodObject = SaareMethods.SaareMethods()        
    saareMethodObject.getDriver("chrome")
    driver = saareMethodObject.driver
'''
from __samplemodule import SaareMethods
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
        startURL = 'https://lenskart.com?s=1111'
        
        ''' create object of class '''
        saareMethodObject = SaareMethods.SaareMethods()
        
        'get max threads tp parse '
        maxThreads = int(saareMethodObject.get_config_param('crawler', 'max_threads'))
        
        print('using max threads ==> ', maxThreads)

        print('started crawling ---> ') 
        saareMethodObject.performTaskWithoutBrowser(startURL)
        
        ' ===> this condition need to be fixed -- to review'
        with ThreadPoolExecutor(max_workers=maxThreads) as executor:
            while len(saareMethodObject.globalUrlMap) > 0:
                executor.submit(saareMethodObject.launchCrawlerUsingMap)                
        
        print()
        print('Length of global list after crawling ==> ', len(saareMethodObject.globalTraversedSet) , ' Length of global DAMN map after crawling ' , len(saareMethodObject.damnPagesMap))

    except Exception as err:
        traceback.print_exc(file=sys.stdout)
    
    st2 = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print('end time ==> '+st2 + ' start time ==> '+st1 + ' ===> dammn map ===> ', )
    
    print(saareMethodObject.damnPagesMap)
    
    
    
    
    