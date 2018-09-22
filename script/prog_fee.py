import time

class fee_conf:
    port = ""
    scrods = ""
    special_scrod = ""
    scrod_firmware = ""

    dataConcentrator = ""
    dataConcentrator_Firmware = ""

def HandleBrokenScrod(ftsw,FileName,Scrod,port):
    tries = 10
    ret =""
    for i in range(tries):
        x = ftsw.program_devices(FileName,Scrod,port)
        ret += x

        if "3cec" in x:
            ftsw.debugPrint("Programming Successfull")
            return ret
        
        if "1cec" in x:
            ftsw.debugPrint("failed at try "+str(i))
        
        else:
            raise Exception("something wrong at try "+str(i))
            
    raise Exception("Unable to program scrod "+ str(Scrod)+" after "+str(tries)+ " tries",x)


def prog_fee(ftsw,config=fee_conf()):
    ret = ""
    ret += ftsw.program_devices(config.scrod_firmware,config.scrods,config.port)
    ret += HandleBrokenScrod(ftsw,config.scrod_firmware,config.special_scrod,config.port)    
    
    ret += ftsw.program_devices(config.dataConcentrator_Firmware,config.dataConcentrator,config.port)
    time.sleep(2)
    ret +=ftsw.reset() 
    return ret