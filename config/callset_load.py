import pandas as pd

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from config.ftsw_load_config import ftsw_load_config



def callset_load(file_name,KLM_Conf):
    C_KLM  = pd.read_excel(io=file_name, sheet_name="C_KLM")
    conf1 = pd.DataFrame([KLM_Conf])
    C_KLM1  =pd.merge(conf1, C_KLM,left_on=0, right_on='Name') 
    C_Target_X  = pd.read_excel(io=file_name, sheet_name="C_Target_X")
    C_KLM_Target  =pd.merge(C_KLM1, C_Target_X,left_on="C_Target_X", right_on='Name') 
   
    C_CAL_Files  = pd.read_excel(io=file_name, sheet_name="C_CAL_Files")
    HSLB = pd.read_excel(io=file_name, sheet_name="HSLB")
    C_CAL_Files_HSLB  =pd.merge(C_CAL_Files, HSLB,left_on="HSLB", right_on='HSLB_conf') 
    Regions= pd.read_excel(io=file_name, sheet_name="Regions")
    C_CAL_Files_Regions  =pd.merge(C_CAL_Files_HSLB, Regions,left_on="Region", right_on='Name') 
    C_KLM_Target

