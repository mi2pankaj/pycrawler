'''
Created on 08-May-2018

@author: pankaj.katiyar
'''
import configparser

class MyClass(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        con = configparser.ConfigParser()
        con.read("/Users/pankaj.katiyar/Desktop/Automation/PythonCrawler/config/config.ini")
    
        self.con = con
    
    
    def __getkey__(self, section, key):
        dd=self.con.get(section, key)
        
        return dd
    
    
    
        