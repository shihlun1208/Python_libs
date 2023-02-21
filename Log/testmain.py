import sys
import os
if not __package__:
    path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    sys.path.insert(0, path)

import Library.globalvar.globalv as gv
import Library.Log.defaults as logdefaults

if __name__ == "__main__":
    gv.init()
    gv.init_logger()
    
    gv.glogger.logdir_create(logdir="")
    gv.glogger.log_add(
            logfilename="MainFile", 
            loglevel=logdefaults.LOGLVL_DEBUG,
            logfilter="Main",
            rotation= "100 KB")
    
    main_logger = gv.glogger.log_bind(_script_name="[MAIN]", log_to_main=True)
    main_logger.debug("It's a main test.")