
from os import stat


def init():
    global globaldict
    globaldict = dict()
    
def ini_info(name):
    globaldict[name] = None

def get_info(name):
    return globaldict[name]

def set_info(name,value):
    globaldict[name] = value

def del_info(name):
    del globaldict[name]

def init_logger():
    from Library.Log.mylogger import Logger as _Logger
    global glogger
    glogger = _Logger()