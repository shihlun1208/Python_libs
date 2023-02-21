import os
import re
import enum
import traceback
import threading
import time

from loguru import logger
from Library.Log.mylogger import Logger as _Logger
import Library.Log.defaults as logdefaults
import Library.globalvar.globalv as gv

class Thread2(threading.Thread):
    def __init__(self, *args):
        super(Thread2,self).__init__()
        try:
            print ('The value of __name__ is ' + __name__)
            # gv.glogger.log_add(
            #     logfilename="THD2File", 
            #     loglevel=logdefaults.LOGLVL_DEBUG,
            #     logfilter="Thd2",
            #     rotation= "100 KB")
            self.thread2_logger = gv.glogger.log_bind(_script_name="[THREAD2]", log_to_main=True)
            self.thread2_logger.info("Thread 2 - Contextualize your logger easily")
        except:
            traceback.print_exc()

    def run(self):
        self.func()
            
    def func(self):
        try:
            self.thread2_logger.info("test")
        except:
            traceback.print_exc()