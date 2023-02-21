import pandas as pd
import traceback

class PandaDf():
    def __init__(self):
        try:
            self.df = pd.DataFrame()
        except:
            traceback.print_exc()
            
    def read_csv(self, file_path):
        try:
            self.df = pd.read_csv(file_path)
        except:
            traceback.print_exc()
    
    def print_head(self, lines=5):
        try:
            return self.df.head(lines)
        except:
            traceback.print_exc()
            
    def print_tail(self, lines=5):
        try:
            return self.df.tail(lines)
        except:
            traceback.print_exc()

    def sort_values(self, colum_list=list(), asc=True):
        try:
            self.df = self.df.sort_values(by=colum_list, ascending=asc)
        except:
            traceback.print_exc()
    
    def loc_row_datas(self, column, oper, value):
        """
        
        Ref: https://www.statology.org/pandas-select-rows-based-on-column-values/
        Args:
            column (string): column name
            oper (string): |in|, |=|, |>|, |<|
            value 
                (list): used when oper is 'in'
                (int or string) '=', '>', '<'
        """
        try:
            if oper == "in":
                return self.df.loc[self.df[column].isin(value)]
            elif oper == "=":
                return self.df.loc[self.df[column] == (value)]
            elif oper == ">":
                return self.df.loc[self.df[column] > (value)]
            elif oper == "<":
                return self.df.loc[self.df[column] < (value)]
        except:
            traceback.print_exc()
    
    def get_col_data(self, column=str(), unique=False):
        try:
            if unique:
                return self.df[column].unique()
            else:
                return self.df[column]
        except:
            traceback.print_exc()
    
if __name__ == "__main__":
    logpath = r".\Library\Pandas\test.csv"
    mypd = PandaDf()
    mypd.read_csv(logpath)
    print(mypd.print_head(20))
    # print(mypd.print_tail())
    mypd.sort_values(["Test Run"])
    print(mypd.print_head(20))
    print(mypd.loc_row_datas("DUT ID", "=", "S6M000043249"))
    # mypd.df.info()