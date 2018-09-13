#!/usr/bin/python

import subprocess
import os
import sys
import time
import pickle

from equipment.ScintilatorReadout import ScintilatorReadout
from Linux_Helpers.py_reghs import py_reghs
from Linux_Helpers.remoteshell2 import remoteShell2

import config.registers_DC as  registers_DC
import config.config_hawaii as  config
import Input_checks

##VARIOUS GLOBAL VARIABLES
wait0=60.0/500.0 #original
#wait0=120.0/500.0
#wait0=10.0/500.0
T0=4.0*65536.0/63.5e6
#wait = T0*2.0
wait=wait0
if (T0>wait0):
    wait=T0*2.0+wait0

cpr = remoteShell2(config.copper_tunnel)
reghs = py_reghs(cpr,config.reghs_cpr107)
sci = ScintilatorReadout(reghs)

#put readout into known state, disable triggers
def doInitialize(hs,lane,defaultTh,defaultHV):
    laneNum = int(lane)
    defaultThNum = int(defaultTh)
    defaultHVNum = int(defaultHV)

    
    Input_checks.check_valid_line(laneNum)
    Input_checks.check_valid_threshold(defaultThNum)   
    Input_checks.check_valid_HV_number(defaultHVNum)

    
    sci.set_register(lane,registers_DC.Trigger.index_7,4) # T0=4ms
    sci.set_register(lane,registers_DC.Trigger.index_7,4) # T0=4ms
    sci.set_register(lane,registers_DC.RPC_Parser.index_7 ,0) # set Reg 39 dec masks all asics for readout such that no ASIC produces readable hits- that way pdaq wont generate QT data 
    sci.set_register(lane,registers_DC.RPC_Parser.index_7 ,0) # set Reg 39 dec masks all asics for readout such that no ASIC produces readable hits- that way pdaq wont generate QT data 

    #set default HV + DACs
    EntireCHs=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    EntireAsics=[0,1,2,3,4,5,6,7,8,9]
    sci.set_hv_custom(lane,EntireAsics,EntireCHs,defaultHVNum)
    sci.set_th_custom(lane,EntireAsics,EntireCHs,defaultThNum)

def getScalerVsDAC(hs,lane,asic,ch,defaultTh):
    #test inputs
    laneNum = int(lane)
    asicNum = int(asic)
    chNum = int(ch)
    defaultThNum = int(defaultTh)
    
    
    Input_checks.check_valid_line(laneNum)
    Input_checks.check_valid_asic_nr(asicNum)
    Input_checks.check_valid_channel_nr(chNum)
    Input_checks.check_valid_threshold(defaultThNum)    

    if sci.checkRegInterface(lane) == False:
        print("Skipping scaler vs DAC measurement for\t" + str(hs) + "\tlane " + str(laneNum) + "\tASIC " + str(asicNum) + "\tch " + str(chNum))
        return None

    scalerVsDac = []
    numRW = 2
    numTest = 3

    #measure scaler vs threshold DAC value
    print( "Measuring scaler vs DAC for lane " + str(laneNum) + "\tASIC " + str(asicNum) + " ch " + str(chNum))
    for th in range (3575,3550,-1):
    #for th in range (3700,3500,-1):
        #set threshold multiple times to deal with flakey interface
        for _ in range(0,numRW,1):
            sci.set_threshold(laneNum,asicNum,chNum,th)

        #test scalers multiple times to check for inconsistent results
        freqs = []
        for _ in range(0,numTest,1):
            scalers = None
            for _ in range(0,numRW,1):
                time.sleep(wait) #wait for counters to settle
                scalers=sci.get_scaler(laneNum,asicNum)
            if scalers == None:
                print("Failed to read trigger scaler, DAC " + str(th)) 
                continue 
            freq=scalers/T0/1000.0  #in kHz
            #freqs.append(freq)
            freqs.append(scalers)
            print("DAC " + str(th) + "\tRate " +  str(freq))
        scalerVsDac.append( [th,freqs] )

    #return threshold to default value
    for _ in range(0,numRW,1):
        sci.set_threshold(laneNum,asicNum,chNum,defaultThNum)
    if len(scalerVsDac) == 0 :
        return None
    return scalerVsDac

def runTest(hs):
    #test constants
    
    lane = 1
    defaultTh = 0
    defaultHV = 255

    #stop if register interface is broken
    sci.checkRegInterface(lane)
    if sci.checkRegInterface(lane) == False:
        return None
    #check if sane register values returned
    checkRegs(hs,lane)
    #initialize threshold + HV to effecitivelt OFF
    doInitialize(hs,lane,defaultTh,defaultHV)

    #define results dictionary
    results = {}
 
    #actually measure data

    #multi-channel scaler vs DAC study
    #for asic in [0,1,2,3,4,5,6,7,8,9]:
    for asic in [0]:
        for ch in [0]:
            scalerVsDac = getScalerVsDAC(hs,lane,asic,ch,defaultTh)
            if scalerVsDac != None :
                results[(hs,lane,asic,ch,defaultTh,defaultHV)] = scalerVsDac
    
    #save results dictionary and close file
    outputFile = open('scalerVsThresholdData.pkl', 'wb')
    pickle.dump(results, outputFile)
    outputFile.close()

def runDacScan(link):
    #test constants
   
    lane = 1
    defaultTh = 0
    defaultHV = 255

    #initialize
    for link in ['-a']:
        for lane in [1,2]:
            #stop if register interface is broken
            sci.checkRegInterface(lane)
            
            if sci.checkRegInterface(lane) == False:
                continue
            #initialize threshold + HV to effecitivelt OFF
            doInitialize(link,lane,defaultTh,defaultHV)

    #define results dictionary
    results = {}
 
    #actually measure data
    #multi-channel scaler vs DAC study
    for link in ['-a']:
        for lane in [1,2]:
            #stop if register interface is broken
            sci.checkRegInterface(lane)
            if sci.checkRegInterface(lane) == False:
                continue
            for asic in [0]:
                for ch in [0]:
                    scalerVsDac = getScalerVsDAC(link,lane,asic,ch,defaultTh)
                    if scalerVsDac != None :
                        results[(link,lane,asic,ch,defaultTh,defaultHV)] = scalerVsDac
    
    #save results dictionary and close file
    outputFile = open('outputDacScan_scalerVsThresholdData.pkl', 'wb')
    pickle.dump(results, outputFile)
    outputFile.close()

def runHVTest(link):
    #test constants
    
    lane = 1
    defaultTh = 0
    defaultHV = 255
    numRW = 2

    #stop if register interface is broken
    sci.checkRegInterface(lane)
    if sci.checkRegInterface(lane) == False:
        return None
    #check if sane register values returned
    checkRegs(link,lane)
    #initialize threshold + HV to effecitivelt OFF
    doInitialize(link,lane,defaultTh,defaultHV)

    #define results dictionary
    results = {}
 
    #actually measure data

    #single schannel scalers at various HV DAC
    for asic in [0]:
        for ch in [0]:
            for hvDac in (50,0):
                print("Testing HV DAC " + str(hvDac))
                for _ in range(0,numRW,1):
                    sci.set_HV(lane,asic,ch,hvDac)
                scalerVsDac = getScalerVsDAC(link,lane,asic,ch,defaultTh)
                if scalerVsDac != None :
                    results[(link,lane,asic,ch,defaultTh,hvDac)] = scalerVsDac
                #return to default HV DAC value
                for _ in range(0,numRW,1):
                    sci.set_HV(lane,asic,ch,hvDac)

    #save results dictionary and close file
    outputFile = open('hvScan_scalerVsThresholdData.pkl', 'wb')
    pickle.dump(results, outputFile)
    outputFile.close()

def runTrigTest(link):
    #test constants

    defaultTh = 3400
    defaultHV = 0
    numRW = 2


    #turn off eveything
    EntireCHs=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    EntireAsics=[0,1,2,3,4,5,6,7,8,9]
    for _ in range(0,numRW,1):
        sci.set_hv_custom(1,EntireAsics,EntireCHs,255)
        sci.set_hv_custom(1,EntireAsics,EntireCHs,0)
        sci.set_hv_custom(2,EntireAsics,EntireCHs,255)
        sci.set_hv_custom(2,EntireAsics,EntireCHs,0)

    #turn on single ASICs
    #EntireCHs=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    EntireCHs=[0,8]
    EntireAsics=[0,1,2,3,4,5,6,7,8,9]
    for _ in range(0,numRW,1):
        sci.set_hv_custom(1,EntireAsics,EntireCHs,0)
        sci.set_hv_custom(1,EntireAsics,EntireCHs,3000)
        sci.set_hv_custom(2,EntireAsics,EntireCHs,0)
        sci.set_hv_custom(2,EntireAsics,EntireCHs,3000)

    #turn on single channel in each lane
    #for regRW in range(0,numRW,1):
    #    fset_scint_hv(link,1,0,0,0)
    #    fset_scint_threshold(link,1,0,0,3700)

def runInitialize(hs):
    #test constants
    
    lane = 1
    defaultTh = 0
    defaultHV = 255

    #stop if register interface is broken 
    #checkRegInterface(link,lane)
    
    if sci.checkRegInterface(lane) == False:
        return None 
    #check if sane register values returned
    checkRegs(hs,lane)
    #initialize threshold + HV to effecitivelt OFF
    doInitialize(hs,lane,defaultTh,defaultHV)

def checkRegs(hs,lane):
    laneNum = int(lane)

    Input_checks.check_valid_line(laneNum)

    for test in range(10):
        regNum = int(test)
        rval1=sci.get_register(lane,regNum)
       
        rstr = "REG NUM" + "\t" + str(regNum) + "\t" + "REG VAL" + "\t" + str(rval1)
        print(rstr)

def main():
    print("START TEST SCRIPT")
    reghs = config.reghs_cpr107
    checkRegs(reghs,1)
    runInitialize(reghs)
    runTest(reghs)
    #runHVTest(reghs)
    #runDacScan(reghs)
    #runTrigTest(reghs)
    print("DONE TEST SCRIPT")

if __name__ == '__main__':
    main()