import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
import Linux_Helpers.ssh_host as ssh_host
import Xilinx.remote_impact as remote_impact

class Xilinx_vm(ssh_host.ssh_Host):
    HostName="***"
    UserName="***"
    PassWord="***"

i_cfg = remote_impact.Impact_conf("path/to/your/bitfile.bit",position="2")

remote_impact.Program_FPGA(Xilinx_vm,i_cfg,cleanUp=False)
