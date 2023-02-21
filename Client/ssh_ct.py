
if not __package__:
    import sys
    import os
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), os.pardir)
    sys.path.insert(0, path)
    print(path)
#------------------------------------------------
import time
import os
import traceback
import re
import enum
# import socket
import paramiko
from contextlib import suppress
#------------------------------------------------
from Mylib.Base.thread import ThrdFormat
# from Mylib.Base.thread import ThrdFormat
# from Mylib.Base.progress import Progress
#------------------------------------------------
import Mylib.GlobalVar.globalvar as gv
import Mylib.Regex.regex as reg
#------------------------------------------------

class CmdType(enum.Enum):
    TX_ENABLE = "tx_enable"
    TX_STOP = "tx_stop"
    FCT_ENABLE = "fct_enable"


class PayloadPar(enum.Enum):
    IS_FINISH = "isFinish"
    IS_SUCCESS = "isSuccess"
    BAR_COUNTER = "bar_counter"
    DATA = "data"
    CONNECTION = "conn"


class ThrdSSH(ThrdFormat):
    def __init__(self,
                        ip="",
                        port=22,
                        username="",
                        password=None,
                        cmd=None,
                        cmd_type=None,
                        bol_return=False,
                        chk_value=None,
                        *args
                        ):
        super(ThrdSSH,self).__init__()
        try:                 
            self.ip = ip
            self.port = port
            self.username = username
            self.password = password
            self.cmd = cmd
            self.cmd_type = cmd_type
            self.bol_return = bol_return
            self.chk_value = chk_value
            self.args = args
            
            self.ini_par()
            self.ini_logger()

            self.__initPayloads()            
        except:
            traceback.print_exc()


    # def ini_logger(self):
    #     try:
    #         self.logger = gv.get_logger()                    
    #     except:
    #         traceback.print_exc()

    def __finish__(self):
        self.stop()
        self.payloads.update({
            PayloadPar.IS_FINISH.value: True
        })        

    def __initPayloads(self):
        self.payloads = {
            PayloadPar.IS_SUCCESS.value: None,
            PayloadPar.IS_FINISH.value: None,
            PayloadPar.BAR_COUNTER.value: None,
            PayloadPar.DATA.value: None,
            PayloadPar.CONNECTION.value: None
        }    

    def ini_par(self):
        try:
            self.bol_conn = False
        except:
            traceback.print_exc()

    def run(self):
        try:
            self.process()
        except:
            traceback.print_exc()
        finally:
            self.__finish__()

    def process(self):
        try:
            self.payloads.update({PayloadPar.BAR_COUNTER.value : 1})
            #----------------------------------------------------------------            
            with suppress(paramiko.ssh_exception.AuthenticationException):
                try:
                    client = paramiko.SSHClient()
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    client.connect(self.ip, username=self.username, password=self.password, port=22, timeout=2)
                except Exception as e:
                    client.get_transport().auth_none(self.username)
            stdin, stdout, stderr = client.exec_command("ls -al")
            str_got = stdout.readlines()
            if str_got == "" or str_got == None:
                self.bol_conn = False
            else:
                self.bol_conn = True

            if not self.bol_conn:
                self.payloads.update({  PayloadPar.IS_SUCCESS.value: False,
                                        PayloadPar.CONNECTION.value: False,
                                        PayloadPar.BAR_COUNTER.value: 100
                })
                return
            else:
                self.payloads.update({  
                                        PayloadPar.CONNECTION.value: True,
                })
            if self.cmd != None:
                # print("enter command")
                try:
                    stdin, stdout, stderr = client.exec_command(self.cmd)
                except:
                    self.logger.error("[ThrdSSH] exec_command error")
                if self.bol_return:
                    time.sleep(1)
                    str_got = stdout.readlines()
                    # rx_result = self.cmd_rx(self.cmd_type, str_got)
                    # print(str_got)
                    self.payloads.update({PayloadPar.DATA.value: str_got})
                    if self.chk_value is not None:
                        exist = reg.reg_search_if_exist(self.chk_value, str_got)

                        if exist:
                            self.payloads.update({PayloadPar.IS_SUCCESS.value: True,
                                                PayloadPar.BAR_COUNTER.value: 100
                                                })            
                        else:
                            self.payloads.update({PayloadPar.IS_SUCCESS.value: False,
                                                PayloadPar.BAR_COUNTER.value: 100
                                                })
                    else:                           
                        self.payloads.update({PayloadPar.IS_SUCCESS.value: True,
                                PayloadPar.BAR_COUNTER.value: 100
                                })

                    return
            #----------------------------------------------------------------
            self.payloads.update({PayloadPar.IS_SUCCESS.value: True,
                                  PayloadPar.BAR_COUNTER.value: 100
                                  })            
        except Exception:
            traceback.print_exc()
            self.payloads.update({  PayloadPar.IS_SUCCESS.value: False,
                                    PayloadPar.BAR_COUNTER.value: 100
            })

    # def cmd_rx(self, cmd_type=None, value=None):
    #     try:
    #         result = None
    #         bol_return = False
    #         if cmd_type == CmdType.FCT_ENABLE.value:
    #             result = self.__cmd_fct_enable(value)
    #         # elif cmd_type == CmdType.FCT_ENABLE.value:
    #         #     pass
    #         elif cmd_type == CmdType.TX_STOP.value:
    #             pass

    #         return result
    #     except:
    #         traceback.print_exc()


    # def __cmd_fct_enable(self, value):
    #     try:
    #         if len(value):
    #             string = value[0]
    #             if re.search("enable", string):
    #                 return True
    #         return False
    #     except:
    #         traceback.print_exc()



if __name__ == "__main__":
    cmd = 'fct.sh ftm enable'

    cmdgen = ThrdSSH(
                ip = "192.168.11.20",
                username="root",
                cmd=cmd,
                cmd_type=CmdType.FCT_ENABLE.value,
                bol_return=True,
                chk_value="ftm, enable, 0"
                # password=""
    )
    cmdgen.start()
    cmdgen.join()
    print(cmdgen.payloads)


