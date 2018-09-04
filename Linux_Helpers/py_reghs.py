import re
class py_reghs:
    filePath = "reghs" # the location of the reghs command on the computer
    stream = "" # the stream location of the HSLB -abcd
    option = "fee32" 
    timeout = 1
    

def check_return_from_reghs(commandline):
    if "=" not in commandline:
        raise Exception("Unexpected return from Commandpromt. No '=' pressent in = '" + str(commandline) +"'",commandline )
        
def extract_number_from_reghs_return(commandline):
    ret = commandline.split("=")[1]
    ret=ret.splitlines()[0]
    ret = int(ret,16)
    return ret

def reghs_call(shell,reghs_cfg, key, value=""):
    line = reghs_cfg.filePath+ " " +reghs_cfg.stream + " " + reghs_cfg.option + " " +key +" " +value
    shell.sendline(line)
    rootprompt = re.compile('.*[$#]')
    shell.expect([rootprompt,'assword.*: '])
    #print(i)
    #shell.prompt(timeout=reghs_cfg.timeout)
    
    if len(value)>0:
        return None
    
    ret = shell.before
    check_return_from_reghs(ret)
    ret = extract_number_from_reghs_return(ret)
    return ret


def reghs_stream(shell, reghs_cfg, file):
    line = reghs_cfg.filePath+ " " +reghs_cfg.stream + " stream " + file
    shell.sendline(line)
    rootprompt = re.compile('.*[$#]')
    i = shell.expect([rootprompt,'assword.*: '])
    #shell.prompt(timeout=reghs_cfg.timeout)
    return shell.before



def reghs_stream_adapter(shell, hs,arg1,arg2,arg3,arg4,arg5,arg6,arg7,arg8,arg9,arg10,arg11,arg12):
    dummyfile="test.txt"
    s1="perl -e 'printf(\"%%c%%c%%c%%c%%c%%c%%c%%c%%c%%c%%c%%c\", %s,%s, %s,%s,%s,%s,%s,%s, %s,%s,%s,%s)'" %(arg1,arg2, arg3, arg4 ,arg5, arg6 ,arg7,arg8, arg9,arg10, arg11,arg12)
    s1=s1+" > " +dummyfile +" 2>&1"
    shell.sendline(s1)
    reghs_stream(shell,hs,dummyfile)
    ret = shell.before
    #print(ret)   
    return ret
