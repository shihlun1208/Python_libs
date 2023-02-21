if not __package__:
    import sys
    import os    
    path = os.path.join(os.path.dirname(__file__), os.pardir)
    sys.path.insert(0, path)     

import threading
import traceback
#--------------------------------------------
import Library.globalvar.globalv as gv

class ThrdFormat(threading.Thread):
    def __init__(self):
        super(ThrdFormat,self).__init__()
        threading.Thread.__init__(self)  
        self.stop_event = threading.Event()
        self.suspend_event = threading.Event()
        self.lock = threading.Lock()
            
    def stop(self):
        self.stop_event.set()
    
    def is_stopped(self):
        return self.stop_event.is_set()     
        
    def suspend(self):
        self.suspend_event.set()    

    def is_suspend(self):
        return self.suspend_event.is_set()      
        