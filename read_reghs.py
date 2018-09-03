import sys
sys.path.insert(0, '../Linux_Helpers/')

import Linux_Helpers.py_ssh as py_ssh
import getpass
from timeit import default_timer as timer
import config.config as config
from Linux_Helpers.py_reghs import reghs_call


reghs = config.reghs_cpr107


def reghs1(s,reg,value):
    start = timer()
    ret = reghs_call(s,reghs,str(reg),value=value)
    end = timer()
    print(end - start)
    #ret = ret.split("=")[1]
    #ret=ret.splitlines()[0]

    return ret


s=py_ssh.ssh_connect(config.ssh_path)





r = reghs1(s,0x38,"10")
print("<>")
print(r)
print("</>")


r = reghs1(s,0x38,"")
print("<>")
print(r)
print("</>")