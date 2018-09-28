import csv
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from equipment.py_hslb import py_hslb,hslb_config_obj
from config.registers_DC import Run_Control
from Linux_Helpers.ssh_host import get_ssh_host_by_name
from Linux_Helpers.remoteshell2 import remoteShell2





                
                

def filter_for_ROI(ROI_list,ROI_Name):
    return [x for x in ROI_list if x.Region == ROI_Name]

def correct_link_format(link=""):
    if "-" not in link:
        link = "-"+ link
    
    return link




def create_hslb_from_list(ROI_list,Known_hosts):
    hslbs = []
    for c in ROI_list:
        h = hslb_config_obj()
        h.link = correct_link_format(c.HSLB)
        h.FirmwareFile = c.Firmware
        shell = remoteShell2(get_ssh_host_by_name(Known_hosts, c.Host ))
        hslbs.append(py_hslb(shell,h))
    
    return hslbs

def getHostName(shell):
    return shell.sendAndRecieve("hostname")


def getShellsWithHostName(shells,name):
    if isinstance(shells, (list,)):
        ret = []
        for s in shells:
            s_name = getHostName(s)
            if name in s_name:
                ret.append(s)
            
        if ret:
            return ret
    
    else:
        s_name = getHostName(shells)
        if name in s_name:
            ret = []
            ret.append(shells)
            return ret
    
    raise Exception("No Connection to host: "+name,name)



class py_klm_region:
    def __init__(self,RegionName,Known_hosts,klm_region_configs):
        
        self.RegionName =RegionName
        self.klm_region_configs= filter_for_ROI( klm_region_configs, RegionName )
        self.Known_hosts =Known_hosts
        
        
        self.hslbs= create_hslb_from_list(self.klm_region_configs,self.Known_hosts)
        

    def get_hslb(self,link):
        h =  [x for x in self.hslbs if link in x.config.link]
        return h[0]

    def test_link(self,link):
        h = self.get_hslb(link)
        return h.test()

    def test(self):
        ret = ""
        for x in self.klm_region_configs:
            ret += self.test_link(x.HSLB)
            ret += "\n"
        return ret

    def Configure_link(self,conf):
        h = self.get_hslb(conf.HSLB)
        ret =""
        ret += h.test()
        ret += "SCINT_PKT_SZ = " +str(h.reghs(Run_Control.SCINT_PKT_SZ)) + '\n'
        h.reghs_setAndCheck(Run_Control.SCINT_PKT_SZ,conf.RCL_test)
        h.reghs_setAndCheck(Run_Control.SCINT_PKT_SZ,conf.RCL_set)
        ret += h.reghs_stream_file(conf.basePath + "/" + conf.config + "/"+ conf.RCL_file)
        return ret
        #h.reghs_setAndCheck()

    def configure(self):
        ret = ""
        for x in self.klm_region_configs:
            ret += self.Configure_link(x)
            ret += "\n"
        
        return ret
        

        

def get_unique_regions(klm_region_configs):
    ret = []
    for x in klm_region_configs:
        if x.Region not in ret:
            ret.append(x.Region)

    return ret

def create_klm_regions(shells,klm_region_configs,IgnoreMissingShells=False):
    ret = []
    regions = get_unique_regions(klm_region_configs)

    
    for x in regions:
        try:
            ret.append(py_klm_region(x,shells,klm_region_configs))
        except:
            if not IgnoreMissingShells:
                raise
        
    

    return ret

       




        
    




