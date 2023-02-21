if not __package__:
    import sys
    import os    
    path = os.path.join(os.path.dirname(__file__), os.pardir)
    sys.path.insert(0, path)   

import pandas as pd
import traceback
import os
import numpy as np


class PandaCsv():
    def __init__(self, path=""):
        self.dfData = pd.DataFrame()
        self.header = None
        self.row_num = None
        self.header_num = 0
        if path != "":
            self.import_csv(path)

    def is_cell_empty(self, *args):
        try:
            list_column = list(self.dfData.columns)
            for i in range(len(list_column)):
                item = list_column[i]
                if item in args:
                    continue
                for j in range(len(self.dfData)):
                    if type(self.dfData[item][j]) == type(np.nan):
                        return True
            return False

        except:
            traceback.print_exc()
            return False


    def clear_dataframe(self):
        try:
            self.dfData = pd.DataFrame()
            return True
        except:
            traceback.print_exc()
            return False

    def create_file(self, path=""):
        try:
            if os.path.isfile(path) and os.access(path, os.R_OK):
                pass
            else:
                file = open(path, "w") 
                file.close()  
            return True
        except:
            return False


    def export_file(self, path="", data={}, index=False):
        '''
        data = {
                'col1' : [1,3,5],
                "col2" : ["a","b","c"]
            }
        '''
        try:
            if os.path.isfile(path) and os.access(path, os.R_OK):
                os.remove(path)
            if not index:
                frameData = pd.DataFrame(data,index=None)
            else:
                frameData = pd.DataFrame(data)
            frameData.to_csv(path, mode="w", index=None)  
            return True
        except:
            traceback.print_exc()
            return False


    def write_file(self, path="", data={}, index=False):
        try:
            if not index:
                frameData = pd.DataFrame(data,index=None)
            else:
                frameData = pd.DataFrame(data)
            frameData.to_csv(path, mode="w", index=None)  
            return True
        except:
            traceback.print_exc()
            return False

    def import_csv(self, path)->bool:
        try:
            dfData = pd.read_csv(path,dtype=str)
            self.dfData = dfData
            self.header = list(self.dfData.columns.values)
            self.header_num = len(self.header)
            self.row_num = len(self.dfData[self.header[0]].tolist())
            return True
        except:
            traceback.print_exc()
            return False

    def get_header(self)-> list:
        try:
            return list(self.dfData.columns.values)
        except:
            traceback.print_exc()
            return False

    def get_header_index(self, name="")->int:
        try:
            return self.header.index(name)
        except:
            traceback.print_exc()
            return False


    def get_cell_data(self, key="",index=0)-> str:
        '''
        index : 0 -> end
        '''
        try:
            if type(self.dfData[key][index]) == type(""):
                data = self.dfData[key][index]
            else:
                data = self.dfData[key][index].item()
            return data
        except:
            traceback.print_exc()
            return False

    def get_coordi_data(self, row=None, col=None):
        try:
            if col != None:
                return self.dfData.values[row][col]
            else:
                return self.dfData.values[row]
        except:
            traceback.print_exc()
            return False



    def get_col_data(self, key="")-> list:
        '''
        '''
        try:
            return self.dfData[key].tolist()
        except:
            traceback.print_exc()
            return False


    def new_col_data(self, key="", data=[])->bool:
        try:
            self.dfData[key] = data
            self.row_num = len(data)
            return True
        except:
            traceback.print_exc()
            return False


    def set_col_data(self, key="", index=0, data=None)->bool:
        try:
            self.dfData[key][index] = data
            return True
        except:
            traceback.print_exc()
            return False




if __name__ == "__main__":
    from pathlib import Path
    pc = PandaCsv(str(Path.cwd()) + r"\\Pandas\\be_test_set.csv")
    print(pc.dfData)
    result = pc.is_cell_empty()
    print("--------------- get_header example --------------")
    print()
    headerlist = pc.get_header()
    print(headerlist)
    print()

    print("--------------- get_header_index example -------")
    print()
    id = pc.get_header_index(name="Modulation")
    print(id)
    print()

    print("---------------- get_cell_data example ------------")
    print()
    data = pc.get_cell_data(key="Channel", index=0)
    print(data)
    print()

    print("--------------- get_coordi_data example -------------")
    print()
    rowdata = pc.get_coordi_data(row=1)
    print(rowdata)
    print()

    print("----------------- get_col_data example --------------")
    print()
    coldata = pc.get_col_data("Channel")
    print(coldata)
    print()

    print("----------------- new_col_data example --------------")
    print()
    pc.new_col_data("Result",["None", "None", "None", "None"])
    print(pc.dfData)
    print()

    print("----------------- set_col_data example -------------")
    print()
    pc.set_col_data(key="Result", index= 1, data="Test")
    print(pc.dfData)
    print()

