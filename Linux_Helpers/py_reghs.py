import re
import Linux_Helpers.shell as shell

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
    

    
    if len(value)>0:
        shell.sendLine(line)
    else:
        ret = shell.sendAndRecieve(line)
    
        check_return_from_reghs(ret)
        ret = extract_number_from_reghs_return(ret)
        return ret


def reghs_stream(shell, reghs_cfg, file):
    line = reghs_cfg.filePath+ " " +reghs_cfg.stream + " stream " + file
    ret = shell.sendAndRecieve(line)
    return ret
    



def reghs_stream_adapter(shell, hs,arg1,arg2,arg3,arg4,arg5,arg6,arg7,arg8,arg9,arg10,arg11,arg12):
    dummyfile="streamfiles/test%s%s%s%s%s%s%s%s%s%s%s%s.txt" %(arg1,arg2, arg3, arg4 ,arg5, arg6 ,arg7,arg8, arg9,arg10, arg11,arg12)
    dummyfile = dummyfile.replace('0x','')
    #s1="perl -e 'printf(\"%%c%%c%%c%%c%%c%%c%%c%%c%%c%%c%%c%%c\", %s,%s, %s,%s,%s,%s,%s,%s, %s,%s,%s,%s)'" %(arg1,arg2, arg3, arg4 ,arg5, arg6 ,arg7,arg8, arg9,arg10, arg11,arg12)
    #s1=s1+" > " +dummyfile +" 2>&1"
    #shell.sendLine(s1)
    ret = reghs_stream(shell,hs,dummyfile)
    print (ret)
    if "directory" in ret:
        s1="perl -e 'printf(\"%%c%%c%%c%%c%%c%%c%%c%%c%%c%%c%%c%%c\", %s,%s, %s,%s,%s,%s,%s,%s, %s,%s,%s,%s)'" %(arg1,arg2, arg3, arg4 ,arg5, arg6 ,arg7,arg8, arg9,arg10, arg11,arg12)
        s1=s1+" > " +dummyfile +" 2>&1"
        shell.sendLine(s1)
        ret = reghs_stream(shell,hs,dummyfile)
        print (ret)
        if "directory" in ret:
            raise Exception("unable to load stream file "+dummyfile)

    print(ret)   
    return ret
