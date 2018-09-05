import os
import sys
import subprocess
import time
import Linux_Helpers.py_ssh as py_ssh
import re

class baseShell:
    def sendLine(self, line):
        pass
    
    def sendAndRecieve(self,line):
        pass
    
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



class remoteShell(baseShell):
    def __init__(self, ssh_path2host,elevate_shell=False, debugPrintouts=False):
        self.shell = py_ssh.ssh_connect(ssh_path2host,elevate_shell,debugPrintouts)

    def sendLine(self,line):
        self.shell.sendline(line)
        rootprompt = re.compile('.*[$#]')
        self.shell.expect([rootprompt,'.*: '])
        self.shell.before
    

    def sendAndRecieve(self,line):
        self.shell.sendline(line)
        rootprompt = re.compile('.*[$#]')
        self.shell.expect([rootprompt,'.*: '])
        ret = self.shell.before
        return ret

