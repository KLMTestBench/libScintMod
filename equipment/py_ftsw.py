import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from Linux_Helpers.shell import baseShell
from config.registers_DC import ftsw_register

    
class ftsw_conf:
    ID = 00

class ftsw_conf_obj:
    def __init__(self):
        self.ID = 00

def create_ftsw(shell_factory, ftsw_conf):
    f_conf = ftsw_conf_obj()
    f_conf.ID = int(ftsw_conf.ID.at[0])

    host_config = str(ftsw_conf.Host.at[0])
    shell = shell_factory.get_shell(host_config)

    ftsw = py_ftsw(shell=shell,conf= f_conf)
    return ftsw



class py_ftsw:
    def __init__(self,shell=baseShell() , conf=ftsw_conf()):
        self.shell=shell
        self.conf=conf
        self.conf.statft_FN = "statft"
        self.conf.resetft_FN = "resetft"
        self.conf.trigft_FN = "trigft"
        self.conf.ttaddr_FN = "ttaddr"
        self.conf.ttaddr_FN_withEKLM = "ttaddr-with-eklm"
        self.conf.jtagft_FN = "jtagft"
        self.conf.regft_FN = "regft"
        self.conf.utimeft_FN = "utimeft"
        self.debug_printouts =False

    def debug(self,flag=True):
        self.debug_printouts = flag

    def debugPrint(self,Line=""):
        if self.debug_printouts:
            print(Line)

    def status(self):
        ret =  self._sendRecieve(self.conf.statft_FN +' -'+ str(self.conf.ID))
        return ret
    
    def utime(self):
        line = self.conf.utimeft_FN + " -" + str(self.conf.ID)
        ret =  self._sendRecieve(line)
        return ret

    def reset(self):
        line = self.conf.resetft_FN +' -'+ str(self.conf.ID)
        ret =  self._sendRecieve(line)
        return ret

    def trigger(self,rate,option="pulse"):
        line = self.conf.trigft_FN +' -'+ str(self.conf.ID)+ " " +option + " " +str(rate) +" -1"
        ret =  self._sendRecieve(line)
        return ret


    def regft(self,register,value):
        if isinstance(value, str):
            value = value.replace('0x','').zfill(8)
        elif isinstance(value,int):
            value = hex(value).replace('0x','').zfill(8)
        else:
            raise Exception("unexpected type. this function only works with strings and ints")

        line = self.conf.regft_FN +' -' + str(self.conf.ID) +  " "+register+" "+value
        ret =  self._sendRecieve(line)
        return ret


    def set_trigger_limiter(self,NumberOfTrigger,timeInMicroSeconds):
        clk_cycle = 0.0078 #Each clock cycle is 7.8 nanoseconds.
        time_in_clk_cycles = int(timeInMicroSeconds/clk_cycle)
        ret = self.regft(ftsw_register.trigger_limiter, hex(NumberOfTrigger).replace('0x','').zfill(2)+hex(time_in_clk_cycles).replace('0x','').zfill(6))
        return ret
        
    def set_lookBackWindow(self,value):
        ret = self.regft(ftsw_register.lookBackWindow, value)
        return ret

    def _check_for_errors(self,line):
        if "usage: jtagft" in line:
            raise Exception("Not configured correctly: wrong Parameter",line)
        
        if "no jtag response" in line:
            raise Exception("Not configured correctly: no jtag response",line)

        if "too many devices found in the jtag chain (probably noise)." in line:
            raise Exception("Not Configures Correctly: 'too many devices found'",line)


    def _read_til_done(self, x):
        ret=''
        while "done" not in x:
            x = self.shell.sendAndRecieveNN("")
            self.debugPrint(x)
            ret += x
        return ret

    def _check_if_file_exist(self,file):
        file_check = self.shell.sendAndRecieve("ls -la "+file)
        self.debugPrint(file_check)
        if "No such file or directory" in file_check:
            raise Exception("could not find file: "+file,file,file_check)
    
    def _sendRecieve(self,line,DoErrorCheck=False):
        x = self.shell.sendAndRecieve(line)
        self.debugPrint(x)
        if DoErrorCheck:
            self._check_for_errors(x)
        return x

    def _get_ttaddr_FN(self, useEKLM):
        if useEKLM:
            ttaddr_FN = self.conf.ttaddr_FN_withEKLM
        else:
            ttaddr_FN = self.conf.ttaddr_FN
        
        return ttaddr_FN

    def reset_ttaddr(self,useEKLM=False):
        ttaddr_FN = self._get_ttaddr_FN(useEKLM)

        ret =''
        ret += self._sendRecieve(ttaddr_FN+" -" + str(self.conf.ID)+" -c")
        ret += self._sendRecieve(ttaddr_FN+" -" + str(self.conf.ID)+" -a")
        return ret

    def prepare_devices(self, devices,useEKLM=False):
        ttaddr_FN = self._get_ttaddr_FN(useEKLM)
        ret = self._sendRecieve(ttaddr_FN+" -" + str(self.conf.ID)+" -u " + devices)
        return ret

    def program_devices(self, file, device_list,port):
        self._check_if_file_exist(file)
        
        ret =''
        ret += self.reset_ttaddr()
        ret += self._sendRecieve(self.conf.ttaddr_FN+" -" + str(self.conf.ID)+" -j " + device_list)

        ret += self._sendRecieve(self.conf.jtagft_FN+" -" + str(self.conf.ID)+" -" +port+" chain",DoErrorCheck=True)
        
        x = self._sendRecieve(self.conf.jtagft_FN+" -" + str(self.conf.ID)+" -" +port+" program "+file,DoErrorCheck=True)
        ret +=x
        ret += self._read_til_done(x)

        self._check_for_errors(ret)


        return ret
