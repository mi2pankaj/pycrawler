'''
Created on 24-Nov-2017

@author: pankaj.katiyar

in any class return variable with self and in other class, create the instance of first class and then use the returned values like:
    saareMethodObject = SaareMethods.SaareMethods()        
    saareMethodObject.getDriver("chrome")
    driver = saareMethodObject.driver
'''

import traceback
import sys
import time
from datetime import datetime

from __samplemodule import SaareMethods


if __name__ == '__main__':
    
    try:
        
        ''' create object of class '''
        saareMethodObject = SaareMethods.SaareMethods()        
        driver = saareMethodObject.getDriver("chrome")
        
    
        st1 = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        
        ''' execute java script to bring browser at the front '''
        driver.implicitly_wait(60)
        driver.execute_async_script("alert('HI')")
        driver.switch_to.alert.accept()
        
        print('started crawling ---> ')        
        saareMethodObject.globalUrlLst.append("https://www.lenskart.com")
        
        for url in saareMethodObject.globalUrlLst:
            saareMethodObject.performTaskWithBrowser(driver, url)
            
        print('Length of global list after crawling ==> ', len(saareMethodObject.globalUrlLst) , ' Length of global DAMN map after crawling ' , len(saareMethodObject.damnPagesMap))

    except Exception as err:
        traceback.print_exc(file=sys.stdout)
         
        pass
    
    driver.quit()
    
    st2 = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print(st1 + " ----  " +st2)
    
    
    
    
    