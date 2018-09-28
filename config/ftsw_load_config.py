import pandas as pd
def ftsw_load_config(file_name,KLM_Global_Config):
    C_KLM = pd.read_excel(io=file_name, sheet_name="C_KLM")
    conf1 = pd.DataFrame([KLM_Global_Config])
    C_KLM1  =pd.merge(conf1, C_KLM,left_on=0, right_on='Name') 
    C_KLM2 = pd.DataFrame(C_KLM1, columns=['Name', 'C_Devices_Conf'])
    C_Devices_Conf = pd.read_excel(io=file_name, sheet_name="C_Devices_Conf")
    C_Devices_Conf1  = pd.merge(C_KLM2,C_Devices_Conf,left_on='C_Devices_Conf', right_on='Name_dev') 
    C_FTSW = pd.read_excel(io=file_name, sheet_name="C_FTSW")
    C_Devices_Conf2  = pd.merge(C_Devices_Conf1,C_FTSW ,left_on='FTSW', right_on='Name') 

    return C_Devices_Conf2
