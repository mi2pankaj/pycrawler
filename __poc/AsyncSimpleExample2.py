'''
Created on 12-Oct-2018

@author: pankaj.katiyar
'''

import aiohttp
import asyncio
import requests
import traceback
import sys

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
    
    
    async def fetch(self, url):
        response = aiohttp.request('GET', url)
        print('response object --> ', response)
        return response
        
        
    async def httpRequest(self, url):
        try:
            print('started request method with url ---> '+url)
            response = await requests.get(url)
            pageSource = response.text
            status_code = response.status_code
            print()
            print('response received from url --> '+ url + " -- status code -- ", status_code, ' and response is ==> ')
            print()
        except Exception:
            print(' ^^^^^^^^^^^^^^^^^ ERROR ^^^^^^^^^^^^^^^^^ WITH ^^^^^^^^ '+url)
            traceback.print_exc(file=sys.stdout)
        
        
    def launch_method1(self):
         
#         loop1 = asyncio.new_event_loop()
#         count1_1 = loop1.create_task(self.print_numbers_async1(10, 'number_1_1'))
#         count1_2 = loop1.create_task(self.print_numbers_async1(10, 'number_2_1'))
          
#         loop1.run_until_complete(asyncio.wait([count1_1, count1_2]))
#         loop1.close()
          
        loop2 = asyncio.new_event_loop()
        count2_1 = loop2.create_task(self.print_numbers_async2(10, 'number_2_1 ==> '))
        count2_2 = loop2.create_task(self.print_numbers_async2(10, 'number_2_2 ==> '))
          
        loop2.run_until_complete(asyncio.wait([count2_1, count2_2]))
        loop2.close()
         
#         loop = asyncio.new_event_loop()
#         count1 = loop.create_task(self.fetch('http://www.google.com'))
#         count2 = loop.create_task(self.fetch('http://www.github.com'))
#         loop.run_until_complete(asyncio.wait([count1, count2]))
#         loop.close()
    
    pass
        
        
                
                