from Linux_Helpers.shell import baseShell
import os
import base64
import paramiko


def get_port(host):
  if hasattr(host, 'port'):
    return int(host.port)
  if hasattr(host, 'Port'):
    return int(host.Port)

  return int(22)

def connect(client,host):
    if host.IdentityFile:
        client.connect(host.HostName,get_port(host),username=host.UserName, key_filename=host.IdentityFile)
    else:
        client.connect(host.HostName,get_port(host),username=host.UserName, password=host.PassWord)

class remoteShell2(baseShell):
  def __init__(self, host, debugPrintouts=False):
    self.host = host
    self.client =  paramiko.SSHClient()
    self.client.load_system_host_keys()
    self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connect(self.client,host)
    
    

  def sendLine(self, line):
    
    stdin, stdout, stderr = self.client.exec_command(line)
    stdout.read()
    stderr.read()
    

  def sendAndRecieve(self,line):
    stdin, stdout, stderr = self.client.exec_command(line)
    x=(stdout.readlines())
    x = ''.join(x)
    y= (stderr.readlines())
    y = ''.join(y)
    x=x+y
    return x
