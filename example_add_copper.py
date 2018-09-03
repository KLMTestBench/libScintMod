import Copper_Helpers.add_copper as add_copper
import Linux_Helpers.py_ssh as py_ssh
import config.config as config



path = (config.IDLab,config.PocketDAQ)
s=py_ssh.ssh_connect(path,elevate_shell=True)




copper_150=add_copper.COPPER_conf(ID_number=150,HardwareAdress="00:00:cc:f0:1d:76")
add_copper.add_copper(s,copper_150)