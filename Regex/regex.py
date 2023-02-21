import re
import traceback


def get_email_regex():
    emailregex = re.compile(r'''(
        [a-zA-z0-9._%+-]+
        @
        [a-zA-z0-9.-]+
        (\.[a-zA-Z]{2,4})
    )''', re.VERBOSE)
    
    return emailregex

# ----------------------------------------
def convert_list_to_str(value):
    if type(value) == list:
        return ''.join(value)
    else:
        return value

def reg_search_if_exist(_string_ ,value):
    try:
        value = convert_list_to_str(value)
        ptn = re.compile('{}'.format(_string_))
        result = ptn.search(value)
        if result:
            return True
        else:
            return False
    except:
        traceback.print_exc()

def reg_search(_string_, value):
    try:
        value = convert_list_to_str(value)
        ptn = re.compile('{}'.format(_string_))
        result = ptn.search(value)
        if result:
            return result.group()
        else:
            return None
    except:
        traceback.print_exc()

def reg_findall(_string_, value):
    try:
        value = convert_list_to_str(value)
        ptn = re.compile('{}'.format(_string_))
        resultlist = ptn.findall(value)
        if resultlist:
            return resultlist
        else:
            return None
    except:
        traceback.print_exc()

def reg_search_btw(_from, _to, value, greedy=False):
    try:
        value = convert_list_to_str(value)
        if greedy:
            ptn = re.compile(r'{}.*{}'.format(_from, _to))
        else:
            ptn = re.compile(r'{}.*?{}'.format(_from, _to))
        result = ptn.search(value)
        if result:
            return result.group()
        else:
            return None
    except:
        traceback.print_exc()

def reg_lookbehind_ahead(_behof, _ahdof, value):
    try:
        value = convert_list_to_str(value)
        result = re.search(r"(?<={behof}).*(?={ahdof})".format(behof = _behof, ahdof = _ahdof), value)
        if result:
            return result.group(0)
        else:
            return None
    except:
        traceback.print_exc()

def reg_search_igncap(_string_, value):
    try:
        value = convert_list_to_str(value)
        ptn = re.compile('{}'.format(_string_), re.I)
        result = ptn.search(value)
        if result:
            return result.group()
        else:
            return None
    except:
        traceback.print_exc()

if __name__ == "__main__":
    phone = "\d\d\d-\d\d\d-\d\d\d\d"
    result = reg_search(phone, "Cell:222-555-9999 Work: 22-555-0000")
    print(result)
    result = reg_findall(phone, "Cell:222-555-9999 Work: 222-555-0000")
    print(result)

    print(reg_search_btw(_from='<', _to='>', value="<To serve man> for dinner.>"))
    print(reg_lookbehind_ahead(_behof='Total', _ahdof='records', value="Total 59 records found. (55 unique DUT-IDs)"))
    print(reg_search_btw(_from='<', _to='>', value="<To serve man> for dinner.>", greedy=True))

    print(reg_search_igncap("robot", "RoBoTo"))