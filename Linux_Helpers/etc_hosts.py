from Linux_Helpers.py_ssh import set_content

class Host:
    def __init__(self,HostName,IP_address,alias="",comment=""):
        self.HostName = HostName
        self.IP_address = IP_address
        self.alias = alias
        self.comment = ""
        if len(comment)>0:
            self.comment = '#' + comment

def add_host(elevated_remoteShell,host):
    line = host.IP_address + " " +host.HostName + " " + host.alias + " " +host.comment
    set_content(elevated_remoteShell,Line=line,FileName='/etc/hosts',Append=True)