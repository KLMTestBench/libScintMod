

def check_valid_HSLB(hs):
    if (hs != "-a") and (hs != "-b") and (hs != "-c") and (hs != "-d"):
        raise Exception("The HSLB Link was not set correctly",hs)

def range_check(Var,VariableName,Begin_r,End_r):
    if Var < Begin_r or Var > End_r :
        raise Exception("The " + VariableName+" was not set Correctly. '"+VariableName+"' = " + str(Var)+ "; It has to be ["+ str(Begin_r)+", " +str(End_r)+"]",Var)




def check_valid_line(laneNum):
    range_check(laneNum,"Line Number",1,2)


def check_valid_asic_nr(asicNum):
    range_check(asicNum,"Asic Number",0,9)


def check_valid_channel_nr(chNum):
    range_check(chNum,"Channel Number",0,14)

def check_valid_threshold(threshold):
    range_check(threshold,"threshold Number",0,4095)

def check_valid_HV_number(HV_number):
    range_check(HV_number,"HV Number",0,255)


def check_valid_DC_number(DC_num):
    range_check(DC_num,"DC Number",0,9)
    
