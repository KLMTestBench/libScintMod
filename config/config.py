
from Linux_Helpers.ssh_host import ssh_Host
from Linux_Helpers.py_reghs import py_reghs

class IDLab(ssh_Host):
    HostName="***"
    PassWord="***"
    UserName="***"

class PocketDAQ(ssh_Host):
    HostName="***"
    PassWord="***"
    UserName="***"

class copper(PocketDAQ):
    HostName="***"
    

class reghs_cpr107(py_reghs):
    filePath="/usr/local/bin/reghs"
    stream="-b"
    timeout=0.1

ssh_path = (IDLab,PocketDAQ,copper)