
import os
import re
import tarfile
import gzip
import shutil
import argparse  
import time
from pathlib import Path
import traceback
import time
import datetime

def extract_targz(extract_path):
    try:
        print("Extracting .tar.gz file...")
        for path in Path(extract_path).rglob('*.tar.gz'):
            print(path)
            full_path_directory = os.path.dirname(str(path))
            # filename = path.name[:-7]
            
            # open file
            file = tarfile.open(str(path))
            # extracting file
            # file.extractall(full_path + "\\" + filename)
            file.extractall(full_path_directory)
            file.close()
    except:
        traceback.print_exc()
        
def extract_gz(extract_path):
    try:
        print("Extracting .gz file...")
        for path in Path(extract_path).rglob('*.gz'):
            if re.search("tar.gz", str(path.name)):
                continue
            print(path)
            full_path_directory = os.path.dirname(str(path))
            with gzip.open(str(path), 'rb') as f_in:
                with open(full_path_directory + "\\" + path.name[:-3], 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
    except:
        traceback.print_exc()

def parse_string_in_logcat(extract_path, parse_string=""):
    try:
        print("Parsing \"{}\" in logcat file...".format(parse_string))
        output_fn = 'Parse_{}_InLogcat.txt'.format(parse_string)
        with open(output_fn,'w+') as g:
            for path in Path(extract_path).rglob('*.txt'):
                print(path)
                if re.search("logcat", str(path.name)):

                    g.writelines(str(path) + "\n")
                    set_warn = False
                    with open( str(path),'r') as file_in:
                    #     g.writelines(filter(lambda line: parse_string in line, file_in))
                        lines = file_in.readlines()
                        for line in lines:
                            if re.search(parse_string, line):
                                g.writelines(line)      

                                if re.search("PHY Link", parse_string):
                                    timestamp = re.findall(r'\d+\:\d+\:\d+', line)
                                    if timestamp:
                                        x = time.strptime(timestamp[0],'%H:%M:%S')
                                        seconds = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
                                        if seconds > 20:
                                            set_warn = True
                    if set_warn:
                        g.writelines("*SET WARNING HERE.*\n")
                    g.writelines("\n")
    except:
        traceback.print_exc()

def parse_string_in_runinlog(extract_path, parse_string=""):
    try:
        print("Parsing \"{}\" in runin log...".format(parse_string))
        output_fn = 'Parse_{}_InRuninLog.txt'.format(parse_string)
        with open(output_fn,'w+') as g:
            for path in Path(extract_path).rglob('*runin.log'):
                print(path)
                # if re.search("runin", str(path.name)):

                g.writelines(str(path) + "\n")
                set_warn = False
                with open( str(path),'r') as file_in:
                    lines = file_in.readlines()
                    for line in lines:
                        if re.search(parse_string, line):
                            g.writelines(line)      
                if set_warn:
                    g.writelines("*SET WARNING HERE.*\n")
                g.writelines("\n")
    except:
        traceback.print_exc()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='extract tar zip file')
    parser.add_argument(
        '-p', '--extract_path', required=True, type=str, help='extract path')
    parser.add_argument(
        '-lcpar', '--logcat_parse', required=False, type=str, help='Parse specific string in Logat.txt')
    parser.add_argument(
        '-ripar', '--runin_logparse', required=False, type=str, help='Parse specific string in runin.log')
    args = parser.parse_args()
    
    extract_targz(args.extract_path)
    extract_gz(args.extract_path)
    if args.logcat_parse is not None:
        parse_string_in_logcat(args.extract_path, args.logcat_parse)
    if args.runin_logparse is not None:
        parse_string_in_runinlog(args.extract_path, args.runin_logparse)
    # path = "."
    # extract_targz(path)
    # extract_gz(path)
    print("============= Finish =============")
    time.sleep(1)
    
    
    
    # parser.add_argument(
    #     'action', choices=['add', 'modify', 'delete'], help='action of upstream nodes, one of add, modify, delete')
    # parser.add_argument(
    #     '-n', '--name', required=True, type=str, help='upstream node name')
    # parser.add_argument(
    #     '-l', '--loki_id', required=False, type=int, help='loki id')
    
    
    # if args.action == "add":
    #     print (args.name, args.loki_id, args.port, args.ip_hash, args.online)
    # elif args.action == "modify":
    #     _dict = {}
    #     for i in ["loki_id", "port", "ip_hash", "online"]:
    #         if getattr(args, i) is not None:
    #             _dict[i] = getattr(args, i)
    #     print (args.name, _dict)
    # elif args.action == "delete":
    #     print (args.name)