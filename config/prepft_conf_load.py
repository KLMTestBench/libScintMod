import pandas as pd

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from config.ftsw_load_config import ftsw_load_config

class prepft_conf:
    def __init__(self):
        self.devices = ""
        self.lookBackWindow = 0
        self.TL_NumberOfTrigger = 0
        self.TL_timeInMicroSeconds = 0
        self.use_EKLM = False


def Dev_details_load(file_name,KLM_Global_Config):
    ftsw_conf = ftsw_load_config(file_name,KLM_Global_Config)


    C_Devices_Details  = pd.read_excel(io=file_name, sheet_name="C_Devices_Details")
    C_Devices_Details1  = pd.merge(ftsw_conf,C_Devices_Details ,left_on='Name_dev', right_on='C_Devices_conf') 
    S_DEVICES = pd.read_excel(io=file_name, sheet_name="S_DEVICES")
    C_Devices_Details2  = pd.merge(C_Devices_Details1,S_DEVICES ,left_on='C_Devices', right_on='Name') 
    
    
    ret = prepft_conf()
    ret.devices = ','.join(list(C_Devices_Details2.C_Devices))
    ret.TL_timeInMicroSeconds = ftsw_conf.TL_timeInMicroSeconds.at[0]
    ret.TL_NumberOfTrigger = ftsw_conf.TL_NumberOfTrigger.at[0]
    ret.lookBackWindow = ftsw_conf.lookBackWindow.at[0]
    ret.use_EKLM = ftsw_conf.use_EKLM.at[0]


    return ret