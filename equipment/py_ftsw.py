import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from Linux_Helpers.shell import baseShell

class ftsw_conf:
    ID = 00


class py_ftsw:
    def __init__(self,shell=baseShell() , conf=ftsw_conf()):
        self.shell=shell
        self.conf=conf
        self.conf.statft_FN = "statft"
        self.conf.resetft_FN = "resetft"
        self.conf.trigft_FN = "trigft"

    def statft(self):
        ret =  self.shell.sendAndRecieve(self.conf.statft_FN +' -'+ str(self.conf.ID))
        return ret
    
    def resetft(self):
        ret =  self.shell.sendAndRecieve(self.conf.resetft_FN +' -'+ str(self.conf.ID))
        return ret

    def trigft(self,rate,option="pulse"):
        line = self.conf.trigft_FN +' -'+ str(self.conf.ID)+ " " +option + " " +str(rate) +" -1"
        ret =  self.shell.sendAndRecieve(line)
        return ret