import os
import traceback
import datetime

def make_dir_bydate(path):
    try:
        # by date
        mydir = os.path.join(
            path,
            datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        os.makedirs(mydir)
        return mydir
    except:
        traceback.print_exc()
        
def make_dir(path):
    try:
        os.makedirs(path)
        return path
    except:
        traceback.print_exc()