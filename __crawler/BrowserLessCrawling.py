'''
Created on 24-Nov-2017

@author: pankaj.katiyar

in any class return variable with self and in other class, create the instance of first class and then use the returned values like:
    saareMethodObject = SaareMethods.SaareMethods()        
    saareMethodObject.getDriver("chrome")
    driver = saareMethodObject.driver
'''
from __crawler import SaareMethods
'''
use regex to (?<=href=").*?(?=") to find out the url in response and add them in a list if starts with http
'''

import time
from datetime import datetime


if __name__ == '__main__':
    
    st1 = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    startURL = 'https://lenskart.com'
    
    'create object of class'
    saareMethodObject = SaareMethods.SaareMethods()
    saareMethodObject.entryMethod(startURL)
    
    st2 = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print('end time ==> '+st2 + ' start time ==> '+st1 + ' ===> dammn map ===> ',saareMethodObject.globalDamnPagesMap)
    
    
    pass