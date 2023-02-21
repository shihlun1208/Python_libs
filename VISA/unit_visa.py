if not __package__:
    import sys
    import os    
    path = os.path.join(os.path.dirname(__file__), os.pardir)
    sys.path.insert(0, path)   

import os
import threading
import enum
import traceback
import time
import re
import pyvisa as visa
import logging
import logging.config
#--------------------------------------------------------------
import Mylib.GlobalVar.globalvar as gv
#--------------------------------------------------------------
# Debug
# logging.config.fileConfig(os.getcwd() + "\\config\\logging.conf")
# self.logger = logging.getLogger("sampleLogger")
#----------------------------------------------------

class FormatType(enum.Enum):
    TCP_1 = "tcp_1"
    TCP_2 = "tcp_2"


class PayloadUnitVisa(enum.Enum):
    IS_FINISH = "isFinish"
    IS_SUCCESS = "isSuccess"
    DATA = "data"


class Visa_USB():
    def __init__(self, vid="", pid="", device_id=""):
        try:
            self.vid = vid
            self.pid = pid
            self.device_id = device_id
            self.inst = None
            self.is_conn = False
            self.info = None
            self.ini_logger()
        except:
            traceback.print_exc()


    def ini_logger(self):
        try:
            self.logger = gv.get_logger()                    
        except:
            traceback.print_exc()


    def conn(self):
        try:
            if (self.vid == "" or
                self.pid == "" or
                self.device_id == ""):
                self.is_conn = False

            visa_addr = "USB0::{VID}::{PID}::{DEVICE_ID}::INSTR".format(
                VID= self.vid,
                PID= self.pid,
                DEVICE_ID= self.device_id
            )
            rm = visa.ResourceManager()
            self.inst = rm.open_resource(visa_addr)
            self.inst.write("*CLS")
            self.info = self.inst.query("*IDN?")   
            self.is_conn = True
        except:
            # traceback.print_exc()
            self.is_conn = False





class VISA():
    def __init__(self):
        try:
            self.addr = ""
            self.cmd = ""
            self.inst = None
            self.info = ""
            self.ip = ""
            self.is_conn = False 
            self.ini_logger()
        except:
            self.logger.error("[VISA] initial error")

    def ini_logger(self):
        try:
            self.logger = gv.get_logger()                    
        except:
            traceback.print_exc()

    def conn(self, ip="", format_type=FormatType.TCP_1.value):
        try:
            self.ip = ip
            if format_type == FormatType.TCP_1.value:
                self.addr = self.visa_format_1st(self.ip)

            rm = visa.ResourceManager()
            self.inst = rm.open_resource(self.addr)
            self.inst.write("*CLS")
            self.info = self.inst.query("*IDN?")   
            self.is_conn = True
            self.logger.info("[VISA] Inst Info : %s",self.info)
        except:
            self.is_conn = False
            self.logger.warning("[VISA] connection error")
            # traceback.print_exc()

    # def is_conn(self):
    #     try:
    #         self.inst.write("*CLS")
    #         self.info = self.inst.query("*IDN?")   
    #         self.is_conn = True            
    #     except:
    #         self.is_conn = True
    #         traceback.print_exc()


    def visa_format_1st(self, visa_addr=""):
        try:
            str_format = "TCPIP::" + visa_addr + "::inst0::INSTR"

            # self.logger.info("str_format : %s",str_format)
            return str_format
        except:
            self.logger.exception("visa_format Fail")
            traceback.print_exc()



class ThrdUnitVisa(threading.Thread):
    def __init__(self,  cmd="", 
                        inst= None,
                        rxreturn = False,
                        timeout_ms = 1000
                        ):
        threading.Thread.__init__(self)
        try:
            self.ini_logger()
            self.__initPayloads()
            self.inst = inst
            self.inst.timeout = timeout_ms
            self.cmd = cmd
            self.rxreturn = rxreturn
            self.stop_event = threading.Event()
            self.__initPayloads()
        except:
            traceback.print_exc()
            self.logger.error("[Unit Visa] initial error")

    def __initPayloads(self):
        self.payloads = {
            PayloadUnitVisa.IS_SUCCESS.value: None,
            PayloadUnitVisa.IS_FINISH.value: None,
            PayloadUnitVisa.DATA.value:None
        }

    def ini_logger(self):
        try:
            self.logger = gv.get_logger()                    
        except:
            traceback.print_exc()

    def __finish__(self):
        try:
            self.stop()
            self.payloads.update({
                PayloadUnitVisa.IS_FINISH.value: True,
            })
        except:
            traceback.print_exc()


    def stop(self):
        self.stop_event.set()

    def is_stopped(self):
        return self.stop_event.is_set()

    def run(self):
        try:
            self.process()
            self.__finish__()
        except:
            traceback.print_exc()

 
    def process(self):
        try:
            if self.rxreturn:
                data = self.inst.query(self.cmd)  
                self.payloads.update({
                    PayloadUnitVisa.IS_SUCCESS.value : True,
                    PayloadUnitVisa.DATA.value: data
                })                
            else:
                self.inst.write(self.cmd)                                
                self.payloads.update({
                    PayloadUnitVisa.IS_SUCCESS.value : True
                })
        except:
            self.logger.error("[Unit Visa] cmd error")            
            # traceback.print_exc()
            self.payloads.update({
                PayloadUnitVisa.IS_SUCCESS.value: False
            })            



# if __name__ == "__main__":
#     vs = Visa_USB(
#         vid= "0x2A8D",
#         pid= "0x1C0B",
#         device_id= "MY60110809"
#     )
#     vs.conn()
#     print()




if __name__ == "__main__":
    ip = "169.254.133.187"
    vs = VISA()
    vs.conn(ip,FormatType.TCP_1.value)
    if vs.is_conn:
        print("connected")
    else:
        print("disconnected")

    # cmdgen = ThrdUnitVisa(inst=vs.inst,cmd="*IDN?",rxreturn=True)
    # cmdgen.start()
    # cmdgen.join()
    # print(cmdgen.payloads)





