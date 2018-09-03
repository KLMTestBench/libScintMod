from Linux_Helpers.py_ssh import set_content

class DHCP_client:
    def __init__(self,HostName,hardware_ethernet,fixed_address,option_host_name="",comment=""):
        self.HostName = HostName
        self.hardware_ethernet = hardware_ethernet
        self.fixed_address = fixed_address
        self.comment = ""
        if len(comment)>0:
            self.comment = '#' + comment

        self.option_host_name = option_host_name
        
       

def add_DHCP_client(elevated_remoteShell,DHCP_cl,restart = True):
    line = 	'host ' + DHCP_cl.HostName + " { hardware ethernet " + DHCP_cl.hardware_ethernet + " ; fixed-address " + DHCP_cl.fixed_address+"; "
    if len(DHCP_cl.option_host_name)>0:
        line = line + "option host-name " +DHCP_cl.option_host_name+" ;" 
    
    line = line +  " } " +DHCP_cl.comment
    set_content(elevated_remoteShell,FileName = '/etc/dhcp/dhcpd.conf',Line=line,Append=True)
    if restart:
        elevated_remoteShell.sendline("systemctl restart dhcpd.service")
        
