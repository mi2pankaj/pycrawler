'''
Created on 11-Feb-2019

@author: abc
'''
from junitparser import JUnitXml
import os

if __name__ == '__main__':
    
    os.system('export PATH=$PATH:/home/linuxbrew/.linuxbrew/bin/node; ')
    os.system('/home/linuxbrew/.linuxbrew/bin/newman run /home/abc/Documents/workspace/nykaa_automation/postman/collections/USM-11.postman_collection.json -e /home/abc/Documents/workspace/nykaa_automation/postman/environment/Production.postman_environment.json -r junit')
    
    
    pass