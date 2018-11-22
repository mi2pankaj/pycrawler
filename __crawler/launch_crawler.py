'''
Created on 24-Nov-2017

@author: pankaj.katiyar

in any class return variable with self and in other class, create the instance of first class and then use the returned values like:
    saareMethodObject = __crawler.utills()        
    saareMethodObject.getDriver("chrome")
    driver = saareMethodObject.driver
'''
from __crawler import utills
from __crawler_logging_module.crawler_logging import __py_logger

'''
use regex to (?<=href=").*?(?=") to find out the url in response and add them in a list if starts with http
'''

import time
from datetime import datetime


if __name__ == '__main__':

    __py_logger.info('======================  STARTING NOW ====================================================================')

    st1 = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    startURL = 'https://lenskart.com'
    
    'create object of class'
    saareMethodObject = utills.GenericMethods()
    saareMethodObject.entryMethod(startURL)
    
    st2 = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    
    __py_logger.info(' started crawler at: ==> '+st1 + '  ended at: ==> '+st2)
    __py_logger.info('')
    __py_logger.info(f' ===> dammn map ===> {saareMethodObject.globalDamnPagesMap}')
    __py_logger.info('=========================================================================================================')
    
    pass

