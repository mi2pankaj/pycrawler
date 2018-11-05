'''
Created on 12-Oct-2018

@author: pankaj.katiyar
'''

from __poc import AsyncSampleClass
import asyncio

if __name__ == '__main__':
    
    sampleClassObject = AsyncSampleClass.MyClass()
    
#     loop = asyncio.new_event_loop()
#     
#     loop.run_until_complete(asyncio.wait([loop.create_task(sampleClassObject.httpRequest('https://www.timeanddate.com/worldclock/india/new-delhi')),
#     loop.create_task(sampleClassObject.httpRequest('http://www.google.com')),
#     loop.create_task(sampleClassObject.httpRequest('http://www.github.com')),
#     loop.create_task(sampleClassObject.httpRequest('https://www.lenskart.com'))]))
# 
#     loop.close
    
    sampleClassObject.launch_method1()
    
    pass




