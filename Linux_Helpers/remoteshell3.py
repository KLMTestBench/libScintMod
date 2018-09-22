from Linux_Helpers.shell import baseShell
import os
import base64
import paramiko
import time
import re



def get_port(host):
  if hasattr(host, 'port'):
    return host.port

  return 22

def escape_ansi(line):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)

def Correct_line_ending(line):
    if not line.endswith('\n'):
        line+='\n'
    
    return line

def remove_comand_promt(line,searchFor='\n['):
    index =line.rfind(searchFor) 
    line = line[0:index]
    return line

def remove_comand(line,searchFor='\n'):
    index =line.find(searchFor) 
    line = line[index:]
    return line

class remoteShell3(baseShell):
  def __init__(self, host, debugPrintouts=False):
    self.timeout=1  
    self.readDeley=0.5
    self.client =  paramiko.SSHClient()
    self.client.load_system_host_keys()
    self.client.set_missing_host_key_policy(paramiko.WarningPolicy())
    self.client.connect(host.HostName,get_port(host),username=host.UserName, password=host.PassWord)
    self.chan = self.client.invoke_shell()
    self.chan.set_combine_stderr(True)
    self.bufsize=256
    time.sleep(self.readDeley)
    ret = ''
    while self.chan.recv_ready():
        data = self.chan.recv(self.bufsize)
        b64 = data.decode()
        ret = ret + escape_ansi(b64)
    
    #print(ret)

    

  def sendLine(self, line):
    self.sendAndRecieve(line)
      
      

  def sendAndRecieve(self,line,removePromt=True):
    line = Correct_line_ending(line)
    self.chan.send(line)
    time.sleep(self.readDeley)
    ret = ''
    while self.chan.recv_ready():
        data = self.chan.recv(self.bufsize)
        b64 = data.decode()
        ret = ret + escape_ansi(b64)
    if removePromt:
        ret = remove_comand_promt(ret)
    return ret

  def sendAndRecieveLong(self,line,tries = 5):
    endstr = "endOfCommand"
    ret = ""
    x = self.sendAndRecieve(line+" && echo \""+endstr+"\"")
    x=remove_comand(x)
    current_tries = 0
    while current_tries < tries:
        current_tries+=1
        if not x: #x is empty
            print("empty")
            pass
        elif endstr in x:
            print("found")
            ret += x
            break
        else:
            print("more data")
            ret += x
            current_tries =0
        x =self.sendAndRecieveNN('')
        print(x)
    
    ret=remove_comand_promt(ret,endstr)        
    return ret

  def sendAndRecieveLong2(self,line,SleepFor = 5,removePromt=True):
    dummyFile = "~/dummy.txt"
    ret = ""
    x = self.sendAndRecieve(line+" > " + dummyFile +" 2>&1" )
    ret +=x
    time.sleep(SleepFor)
    x = self.sendAndRecieve("cat " + dummyFile,removePromt)
    ret +=x
    return ret




  def sendAndRecieveNN(self,line,removePromt=True):
    self.chan.send(line)
    time.sleep(self.readDeley)
    ret = ''
    while self.chan.recv_ready():
        data = self.chan.recv(self.bufsize)
        b64 = data.decode()
        ret = ret + escape_ansi(b64)
    if removePromt:
        ret = remove_comand_promt(ret)

    return ret

  def Recieve(self):
    ret = ''
    while self.chan.recv_ready():
        data = self.chan.recv(self.bufsize)
        b64 = data.decode()
        ret = ret + escape_ansi(b64)
    
    return ret
