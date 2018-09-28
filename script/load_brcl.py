import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from equipment.py_hslb import py_hslb,hslb_config_obj
from Linux_Helpers.ssh_host import shell_factory
from config.registers_DC import Run_Control
import _thread
import time
from threading import Thread, Lock

from script.prepdc import prepdc





def load_brcl(shell_factory,RCL,Parallel=False):
    local_Threads = []
    ret = ''
    for i in range(len(RCL.index)):
        e = RCL.iloc[i]
        
        if Parallel:
            t = Thread(target = brcl_configure_link, args = (shell_factory,e,ret))
            t.start()
            local_Threads.append(t)
        else:
            brcl_configure_link(shell_factory,e,ret)
    
    for x in local_Threads:
        x.join()
    
    return ret
        
    
    


def correct_link_format(link=""):
    if "-" not in link:
        link = "-"+ link
    
    return link

basePath="/home/group/b2klm/run/scripts/"






def brcl_create_hslb(sfac,RCL_link_conf):
    h_c = hslb_config_obj()
    h_c.link = correct_link_format(RCL_link_conf.Link)
    shell = sfac.get_shell(RCL_link_conf.Host)
    
    hslb = py_hslb(shell, h_c)
    return hslb


def brcl_execute_configuring_link(hslb,RCL_link_conf):
    ret = hslb.test()
    ret1 =hslb.reghs(Run_Control.SCINT_PKT_SZ)
    ret += RCL_link_conf.HSLB +"  SCINT_PKT_SZ = " +str(ret1) + '\n'
    hslb.reghs_setAndCheck(Run_Control.SCINT_PKT_SZ,RCL_link_conf.SCINT_PKT_SZ_test)
    hslb.reghs_setAndCheck(Run_Control.SCINT_PKT_SZ,RCL_link_conf.SCINT_PKT_SZ_set)
    line = basePath + "/" + RCL_link_conf.configFolder + "/"+ RCL_link_conf.FileName
    #print(line)
    ret += hslb.reghs_stream_file(line)
    #print(ret)
    


def brcl_configure_link(sfac,RCL_link_conf,ret):

    if not RCL_link_conf.Active:
        return
    sucess = False
    
    max_tries = 10
    i = 0
    while not sucess:
        i = i + 1
        if i > max_tries:
            print("unable to configure " +RCL_link_conf.HSLB )
            return

        hslb=None
        try:
            hslb = brcl_create_hslb(sfac,RCL_link_conf)
            brcl_execute_configuring_link(hslb,RCL_link_conf)
            prepdc_ret = prepdc(hslb,RCL_link_conf)
            if 'a' in hslb.config.link:
                print(prepdc_ret)

            sucess = True
            
        except:
            print(RCL_link_conf.HSLB + " Fail")
            time.sleep(1)
        
        finally:
            if hslb:
                sfac.push_shell(hslb.shell)
    
    print("Successfull configured " +RCL_link_conf.HSLB )
         


    
    

    

