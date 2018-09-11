import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
import time
import sys

import Input_checks
import config.registers_DC as registers_DC
import config.ADDRESS_MAP as ADDRESS_MAP
from Linux_Helpers.py_reghs import reghs_call,reghs_stream,reghs_stream_adapter


class ScintilatorReadout:

    def __init__(self,reghs,shell):
        self.reghs = reghs
        self.shell = shell
        self.maxTry = 10
        self.retries = range(self.maxTry)
        self.regWait = 0.01
        self.debug = True

    def get_register_impl(self, lane, reg):
        laneNum = int(lane)
        Input_checks.check_valid_line(laneNum)
        regNum = int(reg)
        reghex = int(ADDRESS_MAP.Scintillator_Mother_t(laneNum).STATUS_START + 2 + regNum)
        ret = reghs_call(self.shell, self.reghs, hex(int(reghex))) 
        time.sleep(self.regWait)
        return ret


    def get_register(self, lane, reg):
        for _ in self.retries:
            val = self.get_register_impl(lane, reg)
            if val != None:
                return val
        
        raise Exception("Unable to read scint registers. Abroad after "+ str(self.maxTry) +" tries. Stream = "+ str(self.reghs.stream) + "; lane = " + str(lane) + "; register = "+str(reg),self.maxTry,self.reghs,lane,reg)

    

    def checkRegInterface(self, lane):
        return True
        #check trigger alive
        sys.stdout.flush()
        rval1 = self.get_register(lane, 0)
    
        time.sleep(1)
        rval2 = self.get_register(lane, 0)
        
        sys.stdout.flush()
        if (rval1==rval2): #PROBLEM - trigger dead - ask user to restart trigger
            print("----DEAD TRIG - RESTART TRIGGER on TTD1----------")
            return False
        print("----REGISTER INTERFACE OK----------")
        return True



    #set SCROD register value
    def set_register(self,lane,reg,val):
        x=int(reg/16)
        y=reg & 15 

        r=(val & 0xf000) / 0x1000 
        t=(val & 0x0f00) / 0x0100 
        q=(val & 0x00f0) / 0x0010 
        w=(val & 0x000f) / 0x0001  
        
        #print lane, reg, val, x, y, r

        reghs_stream_adapter(self.shell,self.reghs, 
        hex(0xf2),   hex(lane*16+0xA), hex(0xf*16+x),
        hex(y*16+r), hex(t*16+q),      hex(w*16+0x8),
        hex(0xf2),   hex(lane*16+0xA), hex(0xf*16+x),
        hex(y*16+r), hex(t*16+q),      hex(w*16+0x8))
        time.sleep(self.regWait)

    #get channel scaler variable
    def get_scaler(self,lane,dc):
        laneNum = int(lane)
        Input_checks.check_valid_line(laneNum)
        
        dcNum = int(dc)
        Input_checks.check_valid_DC_number(dcNum)

        gpL=10 
        gpH=40

        q = self.get_register(laneNum,gpL+dcNum)
        w = self.get_register(laneNum,gpH+dcNum)

        return q+w*65536

    #set channel threshold DAC value
    def set_threshold(self,lane,dc,ch,THval):
        rH=((ch*2) & 0xf0) / 0x10
        rL=((ch*2) & 0x0f) / 0x01
        t=(THval & 0x0f00) / 0x0100
        q=(THval & 0x00f0) / 0x0010 
        w=(THval & 0x000f) / 0x0001

        reghs_stream_adapter(self.shell,self.reghs, 
        hex(0xf2),   hex(lane*16+0xB), hex(dc*16+rH),
        hex(rL*16+0),hex(t*16+q),      hex(w*16+0x8),
        hex(0xf2),   hex(lane*16+0xB), hex(dc*16+rH),
        hex(rL*16+0),hex(t*16+q),      hex(w*16+0x8) )
        time.sleep(self.regWait)

    

    #set channel HV trim DAC value
    def set_HV(self,lane,dc,ch,DACval):
        q=(DACval & 0x00f0) / 0x0010 
        w=(DACval & 0x000f) / 0x0001 
        reghs_stream_adapter(self.shell, self.reghs, 
        hex(0xf2),   hex(lane*16+0xC), hex(0x0*16+dc),
        hex(ch*16+0),hex(0*16+q),      hex(w*16+0x8),
        hex(0xf2),   hex(lane*16+0xC), hex(0x0*16+dc),
        hex(ch*16+0),hex(0*16+q),      hex(w*16+0x8))  
        time.sleep(self.regWait)


    #loop over ASIC + channels
    def set_hv_custom(self,lane,dcs,chs,val):
        for Iasic in dcs:
            for Ich in chs:
                if self.debug:
                    print( "Set HV\t"+str(self.reghs.stream)+"\t"+str(lane)+"\t"+str(Iasic)+"\t"+str(Ich)+"\t"+str(val))
                self.set_HV(lane,Iasic,Ich,val) 
                self.set_HV(lane,Iasic,Ich,val) 

    def set_th_custom(self,lane,dcs,chs,thval):
        for Iasic in dcs:
            for Ich in chs:
                if self.debug:
                    print( "Set DAC\t" + str(self.reghs.stream) + "\t" + str(lane) + "\t" + str(Iasic) + "\t"+str(Ich) + "\t" +str(thval))
                self.set_threshold(lane,Iasic,Ich,thval)
                self.set_threshold(lane,Iasic,Ich,thval)
