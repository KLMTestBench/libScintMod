from  Linux_Helpers.shell import baseShell
import subprocess
import os
import sys

import time

import re

class LocalShell(baseShell):
    regWait = 0.01
    def sendLine(self,line):
        os.system(line)
        time.sleep(self.regWait)
    
    def sendAndRecieve(self,line):
        proc=subprocess.Popen([line," "],shell=True,stdout=subprocess.PIPE)
        ret=proc.communicate()
        time.sleep(self.regWait)
        return ret

