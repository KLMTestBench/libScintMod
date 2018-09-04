import Linux_Helpers.py_ssh as py_ssh
import os

class Impact_conf:
    def __init__(self,fileName,position):
        self.fileName = fileName
        self.position = position



def Program_FPGA(host_cfg, impact_cfg ,cleanUp=True):
    dummyFolderFirmwareFolder = "/home/ise/"
    py_ssh.scp2Remote(host_cfg.PassWord,impact_cfg.fileName,dummyFolderFirmwareFolder,host_cfg.UserName,host_cfg.HostName)
    basename = os.path.basename(impact_cfg.fileName)
    remote_fileName = dummyFolderFirmwareFolder+"/"+basename
    #print("open ssh connection")
    s=py_ssh.get_ssh_connection(host_cfg.HostName,host_cfg.UserName,host_cfg.PassWord)
    ret = Program_FPGA_impl(s,remote_fileName,position=impact_cfg.position,cleanUp=cleanUp)
    optional_cleanUp(cleanUp,s,remote_fileName)
    s.logout()
    return ret




def Program_FPGA_impl(s,BitFile,CommandFileName = "~/dummy.cmd",position =1, cleanUp = True):
    create_CommandFile(s,CommandFileName,position,BitFile)
    Prog_line  = "impact -batch " +CommandFileName #+ ">~/dummy.txt 2>&1" # might be used if the impact printout is to long 
    s.sendline(Prog_line)
    s.prompt()
    ret =  s.before
    optional_cleanUp(cleanUp,s,CommandFileName)
    return ret


def create_CommandFile(remoteShell,CommandFileName,position,BitFile):
    py_ssh.set_content(remoteShell,"setMode -bscan",CommandFileName,Append=False)
    py_ssh.set_content(remoteShell,"setCable -port auto",CommandFileName,Append=True)
    py_ssh.set_content(remoteShell,"Identify -inferir",CommandFileName,Append=True)
    py_ssh.set_content(remoteShell,"identifyMPM",CommandFileName,Append=True)
    if position>1:
        py_ssh.set_content(remoteShell,'assignFile -p 1 -file \\"/home/ise/unknown_0_8.bsd\\"',CommandFileName,Append=True) # not nessesary but can help shortening the output of the impact command 
    position =str(position)
    progCommand = 'assignFile -p ' + position + ' -file \\"' + BitFile +'\\"'
    py_ssh.set_content(remoteShell,progCommand,CommandFileName,Append=True)
    py_ssh.set_content(remoteShell,"Program -p "+position,CommandFileName,Append=True)
    py_ssh.set_content(remoteShell,"quit",CommandFileName,Append=True)

def optional_cleanUp(cleanUp,remoteShell,fileName):
    if cleanUp:
        line = "rm -f " +fileName
        remoteShell.sendline(line)
        remoteShell.prompt(timeout=1)

#ret = Program_scrod("168.105.243.237","ise","****","TopLevel.bit",position=2)
#print(ret)