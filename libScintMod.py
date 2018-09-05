#!/usr/bin/python

#adapted from original code by Isar

import subprocess
import os
import sys
import time
import getpass
import Linux_Helpers.py_ssh as py_sudo_ssh
import config.config_hawaii as config
import Input_checks
import config.registers_DC as registers_DC
import config.ADDRESS_MAP as ADDRESS_MAP
import Linux_Helpers.shell as shell


from Linux_Helpers.py_reghs import reghs_call,reghs_stream,reghs_stream_adapter

reghs = config.reghs_cpr107
#regWait = 0.05
regWait = 0.01
debug = True

s = shell.remoteShell(config.ssh_path)
#s=shell.LocalShell()



#get SCROD register value
def fget_scint_reg(hs, lane, reg):
    laneNum = int(lane)
    Input_checks.check_valid_line(laneNum)
    regNum = int(reg)
    reghex = ADDRESS_MAP.Scintillator_Mother_t(laneNum).STATUS_START + 2 + regNum
    ret = reghs_call(s,hs,hex(reghex)) 
    time.sleep(regWait)
    return ret



def fget_scint_reg_retry(hs, lane, reg):
    maxTry = 10
    val = None
    for _ in range(0,maxTry,1):
        val = fget_scint_reg(hs, lane, reg)
        if val != None:
            return val
    
    raise Exception("Unable to read scint registers. Abroad after "+ str(maxTry) +" tries. Stream = "+ str(hs) + "; lane = " + str(lane) + "; register = "+str(reg),maxTry,hs,lane,reg)

    

def checkRegInterface(hs, lane):
    return True
    #check trigger alive
    sys.stdout.flush()
    rval1 = fget_scint_reg_retry(hs, lane, 0)
  
    time.sleep(1)
    rval2 = fget_scint_reg_retry(hs, lane, 0)
    
    sys.stdout.flush()
    if (rval1==rval2): #PROBLEM - trigger dead - ask user to restart trigger
        print("----DEAD TRIG - RESTART TRIGGER on TTD1----------")
        return False
    print("----REGISTER INTERFACE OK----------")
    return True



#set SCROD register value
def fset_scint_reg(hs,lane,reg,val):
    x=int(reg/16)
    y=reg & 15 

    r=(val & 0xf000) / 0x1000 
    t=(val & 0x0f00) / 0x0100 
    q=(val & 0x00f0) / 0x0010 
    w=(val & 0x000f) / 0x0001  
    
    #print lane, reg, val, x, y, r

    reghs_stream_adapter(s,hs, 
    hex(0xf2),   hex(lane*16+0xA), hex(0xf*16+x),
    hex(y*16+r), hex(t*16+q),      hex(w*16+0x8),
    hex(0xf2),   hex(lane*16+0xA), hex(0xf*16+x),
    hex(y*16+r), hex(t*16+q),      hex(w*16+0x8))
    time.sleep(regWait)

#get channel scaler variable
def fget_scint_scaler(hs,lane,dc):
    laneNum = int(lane)
    Input_checks.check_valid_line(laneNum)
    
    dcNum = int(dc)
    Input_checks.check_valid_DC_number(dcNum)

    gpL=10 
    gpH=40
    #q=fget_scint_reg(hs,lane,gpL+dc) 
    #w=fget_scint_reg(hs,lane,gpH+dc) 
    q = fget_scint_reg_retry(hs,laneNum,gpL+dcNum)
    w = fget_scint_reg_retry(hs,laneNum,gpH+dcNum)

    return q+w*65536

#set channel threshold DAC value
def fset_scint_threshold(hs,lane,dc,ch,THval):
    rH=((ch*2) & 0xf0) / 0x10
    rL=((ch*2) & 0x0f) / 0x01
    t=(THval & 0x0f00) / 0x0100
    q=(THval & 0x00f0) / 0x0010 
    w=(THval & 0x000f) / 0x0001

    reghs_stream_adapter(s,hs, 
    hex(0xf2),   hex(lane*16+0xB), hex(dc*16+rH),
    hex(rL*16+0),hex(t*16+q),      hex(w*16+0x8),
    hex(0xf2),   hex(lane*16+0xB), hex(dc*16+rH),
    hex(rL*16+0),hex(t*16+q),      hex(w*16+0x8) )
    time.sleep(regWait)

    

#set channel HV trim DAC value
def fset_scint_hv(hs,lane,dc,ch,DACval):
    q=(DACval & 0x00f0) / 0x0010 
    w=(DACval & 0x000f) / 0x0001 
    reghs_stream_adapter(s, hs, 
    hex(0xf2),   hex(lane*16+0xC), hex(0x0*16+dc),
    hex(ch*16+0),hex(0*16+q),      hex(w*16+0x8),
    hex(0xf2),   hex(lane*16+0xC), hex(0x0*16+dc),
    hex(ch*16+0),hex(0*16+q),      hex(w*16+0x8))  
    time.sleep(regWait)


#loop over ASIC + channels
def fset_scint_hv_custom(hs,lane,dcs,chs,val):
  for Iasic in dcs:
    for Ich in chs:
      if debug == True:
        print( "Set HV\t"+str(hs.stream)+"\t"+str(lane)+"\t"+str(Iasic)+"\t"+str(Ich)+"\t"+str(val))
      fset_scint_hv(hs,lane,Iasic,Ich,val) 
      fset_scint_hv(hs,lane,Iasic,Ich,val) 

def fset_scint_th_custom(hs,lane,dcs,chs,thval):
  for Iasic in dcs:
    for Ich in chs:
      if debug == True:
        print( "Set DAC\t" + str(hs.stream) + "\t" + str(lane) + "\t" + str(Iasic) + "\t"+str(Ich) + "\t" +str(thval))
      fset_scint_threshold(hs,lane,Iasic,Ich,thval)
      fset_scint_threshold(hs,lane,Iasic,Ich,thval)
