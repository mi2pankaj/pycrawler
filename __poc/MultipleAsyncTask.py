'''
Created on 14-Nov-2018

@author: pankaj.katiyar
'''
import time
import asyncio


async def myTask(i):
    print(" Started Processing Task ==> ",i)
    print()
    time.sleep(i)
    print(" Ended Processing Task ==> ",i)


async def myTaskGenerator():
    for i in range(5):
        
        print('collecting tasks --> ', i)
        asyncio.ensure_future(myTask(i))


if __name__ == '__main__':
    
    print('entered main method ')
    loop = asyncio.get_event_loop()
    
    print('running collected task ')
#     loop.run_until_complete(myTaskGenerator())
    
    loop.run_until_complete(asyncio.gather(*[myTask(i) for i in range(5)]))
    
    loop.close()
    
    print("Completed All Tasks")
    
    pass