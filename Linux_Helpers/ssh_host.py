import math
import pandas as pd
from Linux_Helpers.remoteshell2 import remoteShell2

class ssh_Host:
    ConfigurationName=""
    HostName=""
    PassWord=""
    UserName=""
    port = 22
    startCommand = ("","") #empty list of strings 
    endstring = "\n["
    IdentityFile = None

def convert2IntOrNone(inp):
    if inp:
        inp= int(inp)
    return inp


class ssh_host_obj:
    def __init__(self,host_config):
        self.ConfigName = host_config.ConfigName.at[0]
        self.HostName = host_config.Hostname.at[0]
        self.UserName = host_config.UserName.at[0]
        self.Password = host_config.Password.at[0]
        self.IdentityFile = host_config.IdentityFile.at[0]
        self.Port = host_config.Port.at[0]
        self.endstring = host_config.endstring.at[0]
        self.startCommand = ""#host_config.StartCommands.at[0]
        self.RemoteShell =  host_config.RemoteShell.at[0]

    
def convertKnownHost2ssh_host(Known_hosts,Configuration):
    conf = pd.DataFrame([Configuration])
    known_host1  = pd.merge(Known_hosts, conf ,left_on='ConfigName', right_on=0) 
    
    ret_ssh = ssh_host_obj(known_host1)
    return ret_ssh
        
    
def ConvertNANtoNone(x):
    if isinstance(x,float):
        if math.isnan(x):
            return None
    
    return x

def fillDefault(old,default):
    if old:
        return old
    
    return default    

    




def get_ssh_host_by_name(known_hosts,configName):
    for x in known_hosts:
        if x.ConfigName == configName:
            return x
    raise Exception("Cannot Find Host, " + configName,configName)

def make_connection(known_hosts,ConfigName):
    x=get_ssh_host_by_name(known_hosts,ConfigName)
    if x.DefaultConfig:
        default = make_connection(known_hosts,x.DefaultConfig)
        x.update(default)    
     
    
    return x

def make_all_connections(known_hosts):
    for x in known_hosts:
        make_connection(known_hosts,x.ConfigName)







### Start 


class shell_factory:
    def __init__(self, known_hosts):
        self.known_hosts = known_hosts
        self.shell_list = []


    def run_on(self, host,line):
        shell = self.get_shell(host)
        ret = shell.sendAndRecieve(line)
        self.push_shell(shell)
        return ret



    def get_shell(self, host):
        for shell in self.shell_list:
            if shell.host.ConfigName == host:
                self.shell_list.remove(shell)
                return shell


        conf1 = pd.DataFrame([host])
        host_config  = pd.merge(self.known_hosts, conf1,left_on='ConfigName', right_on=0) 
        if len(host_config.index) == 0:
            raise Exception("unable to find "+host)
        
        ssh_h =  ssh_host_obj(host_config)

        shell = remoteShell2(ssh_h)
        return shell


    def push_shell(self,shell):
        self.shell_list.append(shell)


        


from config.config_make_default_connections import config_make_default_connections


def load_known_host_from_file(FileName):
    Known_hosts = pd.read_excel(io=FileName, sheet_name="Known_hosts")
    config_make_default_connections(Known_hosts)
    return Known_hosts
