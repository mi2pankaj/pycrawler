'''
Created on 22-Nov-2018

@author: pankaj.katiyar

initialize logging here - all the logging configuration is declared here, probably this will go in a configuration file later on.

'''

import logging
import os

# get the log file 
__logfile = os.path.dirname(os.path.abspath(''))+'/logs/pyc.log'
logging.basicConfig(level=logging.NOTSET, filemode='w', filename=__logfile, format=' %(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s ')
__py_logger = logging.getLogger(__name__)

# stop logging from urllib3 and asyncio
logging.getLogger('urllib3.connectionpool').setLevel(logging.CRITICAL)
logging.getLogger('asyncio').setLevel(logging.CRITICAL)
logging.getLogger('chardet.charsetprober').setLevel(logging.CRITICAL)


# logger.setLevel(logging.NOTSET)
# handler = logging.FileHandler('py.log')
# handler.setLevel(logging.NOTSET)
# logger.addHandler(handler)

__py_logger.info('Starting Logger ======> ======> ======> ======> ======> ======> ======> ======> ======>')

# read database here
# records = {'john': 55, 'tom': 66}
# logger.debug('Records: %s', records)
# logger.info('Updating records ...')

# update records here
# logger.info('Finish updating records')

# try:
#     a= 5/0
# except Exception:
#     __py_logger.error('Exception Occurred :: ', exc_info=True)

        
