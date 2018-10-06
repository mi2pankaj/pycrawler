'''
Created on 08-May-2018

@author: pankaj.katiyar
'''

from testmodule.module2 import MyClass
from testmodule import ConfigLoader

if __name__ == '__main__':
    
    print('bhai chal jana ')
    
#     print(sys.path)
    
    print(MyClass().getValueBhai());
    
    print(ConfigLoader.MyClass().__getkey__("general", "get"))
    
    pass