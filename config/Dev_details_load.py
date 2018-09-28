import pandas as pd

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from config.ftsw_load_config import ftsw_load_config

class Dev_details_conf:
    def __init__(self):
        self.port = ""
        self.scrods = ""
        self.scrod_firmware = ""
        self.special_scrod = ""

        self.dataConcentrator = ""
        self.dataConcentrator_Firmware = ""
        
        self.devices = ""
        self.lookBackWindow = 0
        self.TL_NumberOfTrigger = 0
        self.TL_timeInMicroSeconds = 0
        self.use_EKLM = False





def Dev_details_load(file_name,KLM_Global_Config,FrontBack):
    ftsw_conf = ftsw_load_config(file_name,KLM_Global_Config)
    fw = pd.read_excel(io=file_name, sheet_name="Firmware")
    SC_FW_df  = pd.merge(ftsw_conf,fw ,left_on='Scrod_Firmware', right_on='Name') 
    DC_FW_df  = pd.merge(ftsw_conf,fw ,left_on='DC_Firmware', right_on='Name') 

    C_Devices_Details  = pd.read_excel(io=file_name, sheet_name="C_Devices_Details")
    C_Devices_Details1  = pd.merge(ftsw_conf,C_Devices_Details ,left_on='Name_dev', right_on='C_Devices_conf') 
    S_DEVICES = pd.read_excel(io=file_name, sheet_name="S_DEVICES")
    C_Devices_Details2  = pd.merge(C_Devices_Details1,S_DEVICES ,left_on='C_Devices', right_on='Name') 
    FrontBack= pd.DataFrame([FrontBack])
    FrontBack_DF  = pd.merge(C_Devices_Details2,FrontBack ,left_on='FrontBack', right_on=0) 

    scrod = pd.DataFrame(['scrod'])
    scrods  = pd.merge(FrontBack_DF,scrod ,left_on='Type', right_on=0)
    
    DC = pd.DataFrame(['dataConcentrator'])
    DC_DF  = pd.merge(FrontBack_DF, DC ,left_on='Type', right_on=0) 
    specialSCROD= pd.DataFrame([True])
    specialSCRODs  = pd.merge(scrods,specialSCROD ,left_on='special_scrod', right_on=0) 
    special_sc = ','.join(list(specialSCRODs.C_Devices))



    sc = list(scrods.C_Devices)
    scrod_str = ','.join(sc)
    
    dc_l = list(DC_DF.C_Devices)
    dc_str = ','.join(dc_l)
    
    ret = Dev_details_conf()
    ret.dataConcentrator = dc_str
    ret.scrods = scrod_str
    ret.scrod_firmware = SC_FW_df.FileName.at[0]
    ret.dataConcentrator_Firmware = DC_FW_df.FileName.at[0]
    ret.special_scrod = special_sc
    
    ret.port = ','.join(list(set(list(scrods.Port))))

    ret.devices = ','.join(list(C_Devices_Details2.C_Devices))
    ret.TL_timeInMicroSeconds = int(ftsw_conf.TL_timeInMicroSeconds.at[0])
    ret.TL_NumberOfTrigger = int(ftsw_conf.TL_NumberOfTrigger.at[0])
    ret.lookBackWindow = int(ftsw_conf.lookBackWindow.at[0])
    ret.use_EKLM = ftsw_conf.use_EKLM.at[0]
    return ret




