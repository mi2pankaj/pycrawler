'''
Created on 24-Nov-2017

@author: pankaj.katiyar

in any class return variable with self and in other class, create the instance of first class and then use the returned values like:
    saareMethodObject = __crawler.GenericMethods()        
    saareMethodObject.getDriver("chrome")
    driver = saareMethodObject.driver
'''
from __crawler import GenericMethods
'''
use regex to (?<=href=").*?(?=") to find out the url in response and add them in a list if starts with http
'''

import time
from datetime import datetime


if __name__ == '__main__':
    
    st1 = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    startURL = 'https://lenskart.com'
    
    'create object of class'
    saareMethodObject = GenericMethods.GenericMethods()
    saareMethodObject.entryMethod(startURL)
    
    st2 = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print('=========================================================================================================')
    print(' start time ==> '+st1 + 'end time ==> '+st2)
    print()
    print(' ===> dammn map ===> ',saareMethodObject.globalDamnPagesMap)
    print('=========================================================================================================')
    
    pass

