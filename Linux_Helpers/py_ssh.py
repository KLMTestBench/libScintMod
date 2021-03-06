import re

from pexpect import pxssh
import getpass
import os


def debugPrint(doPrint,msg):
    if doPrint:
        print(msg)


def get_ssh_connection(hostname,username,password,port =22,debugPrintouts=False):
    debugPrint(True,"Connecting to host = "+ hostname + " port " + str(port))
    remoteShell = pxssh.pxssh()    
    remoteShell.login(hostname, username, password,port=port)
    return remoteShell




def handle_password_promt(remoteShell,password,debugPrintouts=False):
    rootprompt = re.compile('.*[$#]')
    i = remoteShell.expect([rootprompt,'assword.*: '])
    if i==0:
        debugPrint(debugPrintouts,"didnt need password!")
        pass
    elif i==1:
        debugPrint(debugPrintouts,"sending password")
        remoteShell.sendline(password)
        j = remoteShell.expect([rootprompt,'Sorry, try again'])
        if j == 0:
            pass
        elif j == 1:
            raise Exception("bad password")
    else:
        raise Exception("unexpected output")


    
def ssh(remoteShell,hostname,username,password,debugPrintouts=False):
    debugPrint(debugPrintouts,"ssh to host = "+ hostname)
    remoteShell.sendline("ssh " + username + "@" + hostname )
    handle_password_promt(remoteShell,password,debugPrintouts)

def sudo(remoteShell,password,command,debugPrintouts=False):
    remoteShell.sendline(command)
    handle_password_promt(remoteShell,password,debugPrintouts)

    
    
def scp(Password,Source,Destination):
    line = 'sshpass -p "'+ Password + '" scp -r '+ Source +" "+ Destination
    os.system(line)
    

def scp2Remote(Password,Source,DestinationFolder,UserName,Host):
    Destination=UserName+"@"+Host +":"+DestinationFolder
    scp(Password,Source,Destination)

def set_content(remoteShell,Line,FileName,Append = False):
    FillOp = " > "
    if Append:
        FillOp = " >> "

    Line ='echo "'+  Line + '" ' + FillOp +  FileName
    remoteShell.sendline(Line)
    remoteShell.prompt(timeout=1)


def append_conf_file(s,password,fileName,Line):
    sudo(s,password,'sudo -i')
    set_content(s,Line,fileName,Append=True)
    s.sendline("exit")



def ssh_connect(ssh_hosts_path,elevate_shell=False, debugPrintouts=False):
    h1 = ssh_hosts_path
    shell = get_ssh_connection(hostname=h1.HostName,username=h1.UserName,password=h1.PassWord,port=h1.port,debugPrintouts=debugPrintouts)
    
    
    
    return shell