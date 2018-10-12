'''
Created on 12-Oct-2018

@author: pankaj.katiyar
'''

from __samplemodule import AsyncSampleClass
import asyncio

if __name__ == '__main__':
    
    sampleClassObject = AsyncSampleClass.MyClass()
    sampleClassObject.print_numbers_async1(10, 'First')
#     
#     loop1 = asyncio.new_event_loop()
#     count1_1 = loop1.create_task(sampleClassObject.print_numbers_async1(100, 'number_1_1'))
#     count1_2 = loop1.create_task(sampleClassObject.print_numbers_async1(10, 'number_2_1'))
    
#     loop1.run_until_complete(asyncio.wait([count1_1, count1_2]))
#     loop1.close()
    
    loop2 = asyncio.new_event_loop()
    count2_1 = loop2.create_task(sampleClassObject.print_numbers_async2(10, 'number_2_1'))
    count2_2 = loop2.create_task(sampleClassObject.print_numbers_async2(10, 'number_2_2'))
    
    loop2.run_until_complete(asyncio.wait([count2_1, count2_2]))
    loop2.close()
    
#     loop2 = asyncio.new_event_loop().create_task(sampleClassObject.print_numbers_async2(33, 'number_2'))
    
    pass

