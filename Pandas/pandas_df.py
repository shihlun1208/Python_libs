if not __package__:
    import sys
    import os    
    path = os.path.join(os.path.dirname(__file__), os.pardir)
    sys.path.insert(0, path)   

import pandas as pd
import numpy as np
import traceback
import os
import logging
import logging.config

#----------------------------------------------------
# Debug
from Mylib.ErrorCode.error_code import ErrorCode
logging.config.fileConfig(os.getcwd() + "\\Mylib\\Cfg\\logging.conf")
logger = logging.getLogger("fileLogger")
#----------------------------------------------------


class PandaDF():
    def __init__(self):
        pass


    @staticmethod
    def get_mask_data(df_data,
                       dst_attri,
                       **kwargs):
        """
        PandaDF.save_mask_data(df_data,
                        "TP",
                        99,
                        Band="2G")

        Parameters
        ----------
        df_data : [type] DataFrame
            [description] the target dataframe
        dst_attri : [type] str
            [description] the target attribute
        value : [type] any
            [description] the target value
        kwargs : mask
        """
     
        try:
            #-----------------------------------------------
            # mask
            value = None
            mask = None
            i = 0
            for attri,limit_value in kwargs.items():
                if i == 0:
                    mask = (df_data[str(attri)]==limit_value)
                else:
                    mask = mask & (df_data[str(attri)]==limit_value)
                i += 1
            #-----------------------------------------------
            index_np64 = list(df_data[mask].index.values)[0]
            index = np.int16(index_np64).item()
            value = df_data.loc[mask, dst_attri]
            return value[index]
        except:
            traceback.print_exc()
            logger.error("%s",ErrorCode.PDF_GET_MASK_DATA.value)


    @staticmethod
    def save_mask_data(df_data,
                       dst_attri, 
                       value,
                       **kwargs):
        """
        PandaDF.save_mask_data(df_data,
                        "TP",
                        99,
                        Band="2G")

        Parameters
        ----------
        df_data : [type] DataFrame
            [description] the target dataframe
        dst_attri : [type] str
            [description] the target attribute
        value : [type] any
            [description] the target value
        kwargs : mask
        """
     
        try:
            #-----------------------------------------------
            # mask
            mask = None
            i = 0
            for attri,limit_value in kwargs.items():
                if type(limit_value) == type(np.nan):
                    continue
                if i == 0:
                    mask = (df_data[str(attri)]==limit_value)
                else:
                    mask = mask & (df_data[str(attri)]==limit_value)
                i += 1
            #-----------------------------------------------
            index_np64 = list(df_data[mask].index.values)[0]
            index = np.int16(index_np64).item()
            df_data.loc[mask, dst_attri] = value
        except:
            traceback.print_exc()
            logger.error("%s",ErrorCode.PDF_SAVE_MASK_DATA.value)    


    @staticmethod
    def drop_mask_data(df_data, **kwargs):
        try:
            #-----------------------------------------------
            # mask
            mask = None
            i = 0
            for attri,limit_value in kwargs.items():
                if type(limit_value) == type(np.nan):
                    continue
                if i == 0:
                    mask = (df_data[str(attri)]==limit_value)
                else:
                    mask = mask & (df_data[str(attri)]==limit_value)
                i += 1
            #-----------------------------------------------
            index_names = df_data[mask].index
            df_data.drop(index_names, inplace=True)
        except:
            traceback.print_exc()
            logger.error("%s",ErrorCode.PDF_DROP_MASK_DATA.value)




if __name__ == "__main__":
    pass
    
    df_data = pd.DataFrame()
    df_data.insert(0,"Radio", ["test"])
    df_data.insert(1,"Band", ["test"])
    df_data.insert(2,"Chain", ["test"])
    df_data.insert(3,"Channel", ["test"])
    df_data.insert(4,"Frequency", ["test"])
    df_data.insert(5,"Rate", ["test"])
    df_data.insert(6,"Rate_BW", ["test"])
    df_data.insert(7,"BW", ["test"])
    df_data.insert(8,"Tech", ["test"])
    df_data.insert(9,"TX_Power", ["test"])
    df_data.insert(10,"Criteria_avg", ["test"])
    df_data.insert(11,"Data_avg", ["test"])
    df_data.insert(12,"avg_PASS/FAIL", ["test"])
    df_data.insert(13,"Criteria_peak", ["test"])
    df_data.insert(14,"Freq_peak", ["test"])
    df_data.insert(15,"Data_peak", ["test"])
    df_data.insert(16,"peak_PASS/FAIL", ["test"])
    df_data.insert(17,"Side", ["test"])

    print("---------------------")
    print(df_data)
    print("---------------------")

    PandaDF.save_mask_data(
                            df_data=df_data,
                            dst_attri="Radio",
                            value=str(11),
                            Frequency="test",
                            BW="test",
                            TX_Power="test",
                            Chain="test",
                            Rate_BW="test",
                            Side="test")
    
    print(df_data)