import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 


from Linux_Helpers.ssh_host import ssh_Host
from Linux_Helpers.py_reghs import reghs_conf
from equipment.py_ftsw import ftsw_conf
from script.prog_fee import fee_conf
from script.prepft import prepft_conf
from equipment.py_hslb import hslb_config




class kek_setup(ssh_Host):
    HostName="127.0.0.1"
    IdentityFile= currentdir+"/b2klm"
    UserName="b2klm"

class ttd11(kek_setup):
    port = 10041
    endstring = "[b2klm@ttd11 ~]"

class klm01(kek_setup):
    port = 10040
    endstring = "b2klm.klm@klm01"

class klmpc02(kek_setup):
    port = 10043

class idlab(klm01):
    startCommand = ("ssh idlab@172.22.18.20","source bashrc-ise.sh")
    endstring="idlab@idlab-klm"


class klm_ftsw(ftsw_conf):
    ID=191

class cpr7001(kek_setup):
    port=17001
    IdentityFile = currentdir+"/cpr700x"

class cpr7002(cpr7001):
    port=17002
        
class cpr7003(cpr7001):
    port=17003
    
class cpr7004(cpr7001):
    port=17004


workingDirektory="/home/belle2/libScintMod/newScripts/"
class SlowControl:
    initFile = workingDirektory+"rcBF3.dat"
    first_reg_value = 10
    second_reg_value = 2400



class klm_fee(fee_conf):
    port = "p0"
    scrods = "s117,s118,s156,s157,s158,s159,s051,s075,s092,s104,s150,s152,s160,s161,s154,s153"
    scrod_firmware = "~/lastfw/180625_klmscint_simple_top_csp.bit"
    special_scrod = "s161"

    dataConcentrator = "dc16,dc17,dc18,dc12,dc13,dc20,dc19"
    dataConcentrator_Firmware = "~/lastfw/concentrator_top_revo_frame9_ec6295315a4.bit"


class klm_fee_BB(fee_conf):
    port = "p1"
    scrods = "s103,s107,s108,s109,s110,s112,s095,s097,s094,s093,s102,s098,s099,s101"
    scrod_firmware = "~/lastfw/180625_klmscint_simple_top_csp.bit"
    special_scrod = "s099"
    
    dataConcentrator = "dc24,dc25,dc26,dc27,dc29,dc21,dc22"
    dataConcentrator_Firmware = "~/lastfw/concentrator_top_revo_frame9_ec6295315a4.bit"


class klm_prepft(prepft_conf):
    devices = "dc16,s117,s118,dc17,s156,s157,dc18,s158,s159,dc12,s160,s161,dc19,s051,s075,dc20,s092,s104,dc13,s150,s152,dc46,dc24,dc25,dc26,s113,s116,s103,s107,s108,s109,s110,s112,dc27,dc29,dc21,dc22,s095,s097,s094,s093,s102,s098,s099,s101"
    lookBackWindow = 0x0c80000
    TL_NumberOfTrigger = 1
    TL_timeInMicroSeconds = 2

class klm_prepft_with_EKLM(prepft_conf):
    devices = "dc16,s117,s118,dc17,s156,s157,dc18,s158,s159,dc12,s160,s161,dc19,s051,s075,dc20,s092,s104,dc13,s150,s152,dc46,dc24,dc25,dc26,s113,s116,s103,s107,s108,s109,s110,s112,dc27,dc29,dc21,dc22,s095,s097,s094,s093,s102,s098,s099,s101,s084,s148,s069,s068,s060,s074,s070,s073,s077,s080,s061,s046,s015,s021,s024,s042,s052,s039,s036,s049,s026,s044,s040,s041,s064,s071,s058,s047,s054,s020,s079,s056,s072,s106,s017,s082,s121,s137,s045,s013,s028,s138,s140,s141,s145,s022,s043,s149,s023,s144,s083,s053,s037,s012,s085,s086,s087,s088,s089,s090,s091,s096,s143,s134,s048,s027,s029,s030,s133,s065,s151,s155,s035,s166,dc15,dc49,dc14,dc30,dc32,dc33,dc34,dc35,dc48,dc37,dc39,dc40,dc41,dc42,dc43,dc44"
    lookBackWindow = 0x0c80000
    TL_NumberOfTrigger = 1
    TL_timeInMicroSeconds = 200
    use_EKLM = True


    

