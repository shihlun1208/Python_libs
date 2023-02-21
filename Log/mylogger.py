import sys
import os
import inspect

from pathlib import Path
if not __package__:
    path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    sys.path.insert(0, path)

from loguru import logger
import Library.Log.defaults as logdefaults
import os
import time
from pathlib import Path

class Logger():
    
    def __init__(self):
        self.LOGLEVEL = None
        logger.configure(extra={"log_filter": None,
                                "scriptname": None})
    
    def loglevel_setall(self, loglevel=logdefaults.LOGLVL_DEBUG):
        """
        LOGLVL_TRACE = "TRACE"
        LOGLVL_DEBUG = "DEBUG"
        LOGLVL_INFO = "INFO"
        LOGLVL_SUCCESS = "SUCCESS"
        LOGLVL_WARNING = "WARNING"
        LOGLVL_ERROR = "ERROR"
        LOGLVL_CRITICAL = "CRITICAL"
        
        Examples
        --------
        >>> loglevel_setall(loglevel=logdefaults.LOGLVL_WARNING)
        """
        self.LOGLEVEL = loglevel
    
    def logdir_create(self, logdir=""):
        """
        logdir : |string|
            path to log directory *** No need timestamp ***
        """
        timestr = time.strftime("%Y%m%d-%H%M%S")
        if logdir == "":
            directory = str(Path.cwd()) + "\\MyLog"
            if not os.path.exists(directory):
                os.mkdir(directory)
            self._logdir = directory +"\\{}".format(timestr)
        else:
            self._logdir = logdir + "\\" + timestr
        os.mkdir(self._logdir)
            
    def log_add(self,
                    logfilename="Main", 
                    loglevel=logdefaults.LOGLVL_INFO,
                    logfilter="Main",
                    **kwargs):
        """
        rotation : |str|, |int|, |time|, |timedelta| or |callable|_, optional
            A condition indicating whenever the current logged file should be closed and a new one
            started.
            
        The ``rotation`` check is made before logging each message. If there is already an existing
        file with the same name that the file to be created, then the existing file is renamed by
        appending the date to its basename to prevent file overwriting. This parameter accepts:
        - an |int| which corresponds to the maximum file size in bytes before that the current
          logged file is closed and a new one started over.
        - a |timedelta| which indicates the frequency of each new rotation.
        - a |time| which specifies the hour when the daily rotation should occur.
        - a |str| for human-friendly parametrization of one of the previously enumerated types.
          Examples: ``"100 MB"``, ``"0.5 GB"``, ``"1 month 2 weeks"``, ``"4 days"``, ``"10h"``,
          ``"monthly"``, ``"18:00"``, ``"sunday"``, ``"w0"``, ``"monday at 12:00"``, ...
        - a |callable|_ which will be invoked before logging. It should accept two arguments: the
          logged message and the file object, and it should return ``True`` if the rotation should
          happen now, ``False`` otherwise.
          
        Examples
        --------
        >>> log_add(logfilename="MainFile", 
                        loglevel=logdefaults.LOGLVL_DEBUG,
                        logfilter="Main",
                        rotation= "100 KB")
        
        """
        if isinstance(self.LOGLEVEL, type(None)):
            _loglevel = loglevel
        else:
            _loglevel = self.LOGLEVEL
        
        kwargsNotNone = {k: v for k, v in kwargs.items() if v is not None}
        
        if logfilter == "Main":
            _filter_format = lambda record: record["extra"].get("log_to_main")
        else:
            _filter_format = lambda record: record["extra"]["log_filter"] == logfilter
        logger.add(self._logdir + "\\" + logfilename + ".log",
                format="{time:YYYY-MM-DD at HH:mm:ss} {extra[scriptname]} [{level}] : {message}",
                filter=_filter_format,
                level=_loglevel,
                **kwargsNotNone)
        
    def log_bind(self, _script_name="", _log_filter="Main", **kwargs):
        """
        _script_name : |string|
            contextualize your logger messages by modifying the extra record attribute (scriptname).
            
        _log_filter : |string|
            bind and filter can control the log wish to write
            
        log_to_main : |bool|
            True : write to Main logs
            thread_2.py, thread_3.py for deatils
        """
        return logger.bind(scriptname=_script_name, log_filter=_log_filter, **kwargs)
    
    def log_disable(self, name):
        """
        name : |string|
            the __name__ of the script
            How to check >>> print ('The value of __name__ is ' + __name__)
        """
        logger.disable(name)
        
    def log_enable(self, name):
        logger.enable(name)
    
if __name__ == "__main__":
    import Library.globalvar.globalv as gv
    from Library.Log.test_script.thread_1 import Thread1
    from Library.Log.test_script.thread_2 import Thread2
    from Library.Log.test_script.thread_3 import Thread3

    # _logger = Logger()
    gv.init()
    gv.init_logger()
    # gv.set_info("Logger", _logger)
    
    # TODO:
    
    # set all log level
    # _logger.loglevel_setall(logdefaults.LOGLVL_INFO)
    
    
    gv.glogger.logdir_create(logdir="")
    gv.glogger.log_add(
            logfilename="MainFile", 
            loglevel=logdefaults.LOGLVL_DEBUG,
            logfilter="Main",
            rotation= "100 KB")

    # disable thread 2 log
    # _logger.log_disable("Library.Log.test_script.thread_2")
    
    main_logger = gv.glogger.log_bind(_script_name="[MAIN]", log_to_main=True)
    main_logger.trace("It's a main test.")
    main_logger.debug("It's a main test.")
    main_logger.info("It's a main test.")
    main_logger.success("It's a main test.")
    main_logger.warning("It's a main test.")
    main_logger.error("It's a main test.")
    main_logger.critical("It's a main test.")
    # cnt = 0
    # while (1):
    #     main_logger.info("It's a main test. - " + str(cnt))
    #     cnt += 1
    # _logger.log_disable("thread_1")

    test1 = Thread1()
    test1.start()
    test2 = Thread2()
    test2.start()
    test3 = Thread3()
    test3.start()
    main_logger.info("Test Done.")