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


def handle_startcommand(chan,startup):
    if isinstance(startup,str):
        x = chan.sendAndRecieve(startup)
        #print(x) 
    else:
        for line in startup:
            x = chan.sendAndRecieve(line)
            #print(x)

def connect(client,host):
    if host.IdentityFile:
        client.connect(host.HostName,get_port(host),username=host.UserName, key_filename=host.IdentityFile)
    else:
        client.connect(host.HostName,get_port(host),username=host.UserName, password=host.PassWord)

class remoteShell3(baseShell):
  def __init__(self, host, debugPrintouts=False):
    self.timeout=1  
    self.readDeley=0.5
    self.conf = host
    self.client =  paramiko.SSHClient()
    self.client.load_system_host_keys()
    self.client.set_missing_host_key_policy(paramiko.WarningPolicy())
    connect(self.client, host)
    self.chan = self.client.invoke_shell()
    self.chan.set_combine_stderr(True)
    self.bufsize=256
    time.sleep(self.readDeley)
    ret = ''
    while self.chan.recv_ready():
        data = self.chan.recv(self.bufsize)
        b64 = data.decode()
        ret = ret + escape_ansi(b64)


    handle_startcommand(self,host.startCommand)


    

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

  def sendAndRecieveLong(self,line,tries = 50,endstr = None):
    if endstr == None:
        endstr = self.conf.endstring

    ret = ""
    x = self.sendAndRecieve(line)
    #print(x)
    x=remove_comand(x)
    #print(x)
    current_tries = 0
    while current_tries < tries:
        current_tries+=1
        if not x: #x is empty
            #print("empty")
            pass
        elif endstr in x:
            #print("found")
            ret += x
            break
        else:
            #print("more data")
            ret += x
            current_tries =0
        x =self.sendAndRecieveNN('',removePromt=False)
        #print(x)
    #print(ret)
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
