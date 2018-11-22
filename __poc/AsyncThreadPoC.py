'''
Created on 05-Nov-2018

@author: pankaj.katiyar
'''
import asyncio
from threading import Thread
from __poc import AsyncSimpleExample2
from __crawler import utills


def start_background_loop(loop):
    
    print('loop is being set up ==> ')
    asyncio.set_event_loop(loop)
    loop.run_forever()
    
    
if __name__ == '__main__':
    
    # Create a new loop
    new_loop = asyncio.new_event_loop()
    
    # Assign the loop to another thread
    t = Thread(target=start_background_loop, args=(new_loop,))
    t.start()
    
    # Give it some async work - 1
    sampleClassObject = AsyncSimpleExample2.MyClass()
    future = asyncio.run_coroutine_threadsafe(sampleClassObject.fetch('http://www.google.com'), new_loop)

    # Give it some async work - 2
    saareMethodObject = utills.GenericMethods()
    future = asyncio.run_coroutine_threadsafe(saareMethodObject.entryMethod('http://www.lenskart.com'), new_loop)
    
    # Wait for the result
    print(future.result())

    pass

