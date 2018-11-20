'''
Created on 20-Nov-2018

@author: pankaj.katiyar
'''

import asyncio 
import time
from datetime import datetime


async def say(something, delay):
    st1 = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    await asyncio.sleep(delay)
    st2 = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print(something+ " , start "+st1 + " end: "+st2)
  
loop = asyncio.get_event_loop()
task1 = loop.create_task(say('First', 8))
task2 = loop.create_task(say('second', 5))

loop.run_until_complete(asyncio.gather(task1, task2))