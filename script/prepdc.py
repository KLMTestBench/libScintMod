import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 


from equipment.py_hslb import py_hslb
from config.registers_DC import DAQ


def prepdc(hslb ,brcl_conf):
    ret = ""
    #hslb = py_hslb()
    
    
    hslb.reghs(DAQ.LKBK_STRT_C,int(brcl_conf.LKBK_STRT_CVAL))
    hslb.reghs(DAQ.LKBK_STOP_C,int(brcl_conf.LKBK_STOP_CVAL))
    hslb.reghs(DAQ.LKBK_STRT_F,int(brcl_conf.LKBK_STRT_FVAL))
    hslb.reghs(DAQ.LKBK_STOP_F,int(brcl_conf.LKBK_STOP_FVAL))
    hslb.reghs(DAQ.LKBK_SCAN,  int(brcl_conf.LKBK_SCAN))

    ret+= "window coarse start: " + str(hslb.reghs(DAQ.LKBK_STRT_C)) +"\n"
    ret+= "window coarse stop: "  + str(hslb.reghs(DAQ.LKBK_STOP_C)) +"\n"
    ret+= "window fine start: "   + str(hslb.reghs(DAQ.LKBK_STRT_F)) +"\n"
    ret+= "window fine stop: "    + str(hslb.reghs(DAQ.LKBK_STOP_F)) +"\n"

    return ret