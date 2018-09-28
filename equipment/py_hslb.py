import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from Linux_Helpers.shell import baseShell
from Linux_Helpers.py_reghs import py_reghs

class hslb_config:
    link=None
    FirmwareFile=""
    FilePath="/usr/local/bin/"
    timeout=0.1
    reghs_options="fee32"

class hslb_config_obj:
    def __init__(self,conf=hslb_config()):
        self.link =conf.link
        self.FirmwareFile= conf.FirmwareFile
        self.FilePath = conf.FilePath
        self.timeout = conf.timeout
        self.reghs_options = conf.reghs_options
    

class py_hslb:
    def __init__(self,shell=baseShell(),hslb_c=hslb_config):
        self.config=hslb_c
        self.shell=shell
        self.reghs_intern = py_reghs(shell,hslb_c)
        

    def status(self):
        line = self.config.FilePath+"staths " + self.config.link
        ret = self.shell.sendAndRecieve(line)
        return ret

    def test(self):
        line = self.config.FilePath+"tesths " + self.config.link
        ret = self.shell.sendAndRecieve(line)
        return ret
        

    def boot(self,FirmWareFile=None):
        if FirmWareFile:
            Firmware=FirmWareFile
        else:
            Firmware=self.config.FirmwareFile
               
        link=self.config.link
        p= self.config.FilePath
        line = p+"booths " + link +" " +Firmware    
        ret = self.shell.sendAndRecieve(line)
        return ret
        

    def reghs(self,key,value=None):
        ret = self.reghs_intern.call(key,value)
        return ret
    
    def reghs_stream_file(self,fileName):
        ret = self.reghs_intern.stream_file(fileName)
        return ret
    
    def reghs_stream(self, arg1,arg2,arg3,arg4,arg5,arg6,arg7,arg8,arg9,arg10,arg11,arg12):
        ret = self.reghs_intern.stream( arg1,arg2,arg3,arg4,arg5,arg6,arg7,arg8,arg9,arg10,arg11,arg12)
        return ret
    
    def reghs_setAndCheck(self,key,value):
        self.reghs(key,value)
        ret = self.reghs(key)
        if ret != value:
            raise Exception("unable to set key="+str(key),key)
            