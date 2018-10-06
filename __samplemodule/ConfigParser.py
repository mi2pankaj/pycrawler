'''
Created on 06-Dec-2017

@author: pankaj.katiyar
'''
import configparser

class ConfigParseKardo(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
        config = configparser.ConfigParser()
        config.read("/Users/pankaj.katiyar/Desktop/Automation/PythonCrawler/config/config.ini")
        self.config = config
    
    
    def get_config_param(self, section, key):
        return self.config.get(section, key)
