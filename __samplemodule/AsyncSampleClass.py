'''
Created on 12-Oct-2018

@author: pankaj.katiyar
'''

import asyncio

class MyClass(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
    
    async def print_numbers_async1(self, n, prefix):
        for i in range(n):
            print(prefix, i)
            
            
    async def print_numbers_async2(self, n, prefix):
        for i in range(n):
            print(prefix, i)
            if i % 5 == 0:
                await asyncio.sleep(0)
                
                
                