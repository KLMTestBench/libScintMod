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
    for i in range(tries):
        x = ftsw.program_devices(FileName,Scrod,port)
        print(x)
        if "3cec" in x:
            ftsw.debugPrint("Programming Successfull")
            return True
        
        if "1cec" in x:
            ftsw.debugPrint("failed at try "+str(i))
        
        else:
            ftsw.debugPrint("something wrong at try"+str(i))
            return False
    raise Exception("Unable to program scrod "+ str(Scrod)+" after "+str(tries)+ " tries",x)


def prog_fee(ftsw,config=fee_conf()):
    print(ftsw.program_devices(config.scrod_firmware,config.scrods,config.port))
    HandleBrokenScrod(ftsw,config.scrod_firmware,config.special_scrod,config.port)    
    
    print(ftsw.program_devices(config.dataConcentrator_Firmware,config.dataConcentrator,config.port))
    time.sleep(2)
    print(ftsw.reset())