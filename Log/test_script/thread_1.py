import os
import re
import enum
import traceback
import threading
import time

from Library.Log.mylogger import Logger as _Logger
import Library.Log.defaults as logdefaults
import Library.globalvar.globalv as gv
from loguru import logger

class Thread1(threading.Thread):
    def __init__(self, *args):
        super(Thread1,self).__init__()
        try:
            self.init_logger()
            self.args = args
            a = 4 / 0
            
            self.thread1_logger.debug("Thread 1 - Contextualize your logger easily")
        except Exception as e:
            self.thread1_logger.opt(exception=True).critical(str(e))
    
    def init_logger(self):
        gv.glogger.log_add(
                logfilename="THD1File", 
                loglevel=logdefaults.LOGLVL_DEBUG,
                logfilter="Thd1",
                rotation= "100 KB")
        self.thread1_logger = gv.glogger.log_bind(_script_name="[THREAD1]", _log_filter="Thd1")
    
    def run(self):
        self.func(4, 0)
        
    def func(self, b, c):
        try:
            self.thread1_logger.error("test")
            a = b / c
        except Exception as e:
            self.thread1_logger.opt(exception=True).critical(str(e))