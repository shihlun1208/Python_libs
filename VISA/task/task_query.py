if not __package__:
    import sys
    import os
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), os.pardir)
    sys.path.insert(0, path)

import traceback

from Library_Foxconn.VISA.unit_visa import ThrdUnitVisa
from Library_Foxconn.VISA.unit_visa import PayloadUnitVisa



def QUERY(inst=None, cmd="", timeout_ms=1000):
    try:
        cmdGen = ThrdUnitVisa(inst=inst,cmd=cmd,rxreturn=True,timeout_ms=1000)
        cmdGen.start()
        cmdGen.join()    
        result = cmdGen.payloads.get(PayloadUnitVisa.IS_SUCCESS.value)
        data = cmdGen.payloads.get(PayloadUnitVisa.DATA.value)
        if result:
            return True,data
        else:
            return False,None
    except:
        traceback.print_exc()
        return False,None




if __name__ == "__main__":
    from Library_Foxconn.VISA.unit_visa import VISA
    from Library_Foxconn.VISA.task.task_write import WRITE
    import UI.Setting.globalvar as gconn
    gconn._init()
    gconn.save_orig_logger_level()
    ip = "169.254.133.187"    
    vs = VISA()
    vs.conn(ip)

    # while 1:
    success,data = QUERY(inst=vs.inst,cmd="*IDN?",timeout_ms=1000)
    # success = WRITE(vs.inst, cmd = ":SYST:PRES")
    success, data = QUERY(vs.inst, cmd = ":SYST:CONF?")
    success, data = QUERY(vs.inst, cmd = ":SYST:ERR?")
    success = WRITE(vs.inst, cmd = ":DISP:WIND:TRAC:Y:RLEV:OFFS 12.7")
    success, data = QUERY(vs.inst, cmd = ":DISP:WIND:TRAC:Y:RLEV:OFFS?")
    success, data = QUERY(vs.inst, cmd = ":DISP:HARM:VIEW:WIND:TRAC:Y:RLEV?")
    
    # success, data = QUERY(vs.inst, cmd = ":SYST:SHOW SYST?")
    # success = WRITE(vs.inst, cmd = "*CLS")
    print(success,data)
    # import re
    # if re.search("DETECTED", data):
    #     break





