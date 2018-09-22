from Linux_Helpers.shell import baseShell
import Linux_Helpers.py_ssh as py_ssh
import subprocess
import os
import sys

import time

import re

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

