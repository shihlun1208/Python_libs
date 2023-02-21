if not __package__:
    import sys
    import os
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), os.pardir)
    sys.path.insert(0, path)

import traceback

from Library_Foxconn.VISA.unit_visa import ThrdUnitVisa
from Library_Foxconn.VISA.unit_visa import PayloadUnitVisa



def WRITE(inst=None, cmd="", timeout_ms=1000):
    try:
        cmdGen = ThrdUnitVisa(inst=inst,cmd=cmd,rxreturn=False,timeout_ms=1000)
        cmdGen.start()
        cmdGen.join()    
        result = cmdGen.payloads.get(PayloadUnitVisa.IS_SUCCESS.value)
        if result:
            return True
        else:
            return False
    except:
        traceback.print_exc()
        return False



if __name__ == "__main__":
    from Library_Foxconn.VISA.unit_visa import Visa_USB
    # from Library_Foxconn.VISA.unit_visa import VISA
    vid = "0x2A8D"
    pid = "0x1C0B"
    device_id = "MY60110809"
    vs = Visa_USB(vid,pid,device_id)
    vs.conn()
    if vs.is_conn:
        inst = vs.inst
        success = WRITE(inst, cmd = "*RST")
        success = WRITE(inst, cmd = "*CLS")

        # success = WRITE(inst, cmd = "DET1 QPEak")
        success = WRITE(inst, cmd = "TRAC1:TYPE MAXH")
        success = WRITE(inst, cmd = "OBW:MAXH ON")
        print()

    else:
        print()


    print(success)



# if __name__ == "__main__":
#     from Library_Foxconn.VISA.unit_visa import VISA
#     ip = "192.168.1.3"    
#     vs = VISA()
#     vs.conn(ip)

#     success = WRITE(inst=vs.inst,cmd="*CLS")
#     print(success)





