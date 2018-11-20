'''
Created on 20-Nov-2018

@author: pankaj.katiyar
'''
import requests
import asyncio
from concurrent.futures.process import ProcessPoolExecutor


def blocking_function():
    print('started ---> ')
    response = requests.get('https://breadcrumbscollector.tech/feed/')
    print(f'Got data of length: {len(response.content)} in just {response.elapsed}')


if __name__ == '__main__':
    
    loop = asyncio.get_event_loop()
    
    #1
    coro = loop.run_in_executor(None, blocking_function)  # will use default threads executor!
    loop.run_until_complete(coro)
    
    
    #2
    with ProcessPoolExecutor() as process_executor:
        coro = loop.run_in_executor(process_executor, blocking_function)
        loop.run_until_complete(coro)
    
    pass