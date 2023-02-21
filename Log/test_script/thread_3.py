import os
import re
import enum
import traceback
import threading
import time
from Library.Log.mylogger import Logger as _Logger
import Library.Log.defaults as logdefaults
import Library.globalvar.globalv as gv

class Thread3(threading.Thread):
    def __init__(self, *args):
        super(Thread3,self).__init__()
        try:
            self.args = args
            gv.glogger.log_add(
                logfilename="THD3File", 
                loglevel=logdefaults.LOGLVL_DEBUG,
                logfilter="Thd3",
                rotation= "100 KB")
            
            self.thread3_logger = gv.glogger.log_bind(_script_name="[Thread3]", _log_filter="Thd3")
            self.thread3_logger.debug("Thread 3 - Contextualize your logger easily")
        except:
            traceback.print_exc()
    
    def run(self):
        self.func()
    
    def func(self):
        try:
            self.thread3_logger.error("test")
            self.thread3_logger.bind(log_to_main=True).success("End of task 3")
            self.thread3_logger.error("test-2")
            self.thread3_logger.warning("test-3")
        except:
            traceback.print_exc()