import pandas as pd
def RCL_Load_Config(file_name,KLM_Conf):
    C_KLM = pd.read_excel(io=file_name, sheet_name="C_KLM")
    C_RCL_global= pd.read_excel(io=file_name, sheet_name="C_RCL_global")
    C_RCL_Link= pd.read_excel(io=file_name, sheet_name="C_RCL_Link")
    C_DC_prepdc = pd.read_excel(io=file_name, sheet_name="C_DC_prepdc")
    HSLB= pd.read_excel(io=file_name, sheet_name="HSLB")
    Regions= pd.read_excel(io=file_name, sheet_name="Regions")
    
    RCL_proto = pd.merge(C_KLM,C_RCL_global,left_on='C_RCL_global', right_on='Name') 
    RCL  = pd.merge(RCL_proto,C_RCL_Link,left_on='C_RCL_Link', right_on='Name') 
    RCL2 = pd.DataFrame(RCL, columns=['Name_x', 'configFolder', 'SCINT_PKT_SZ_test', 'SCINT_PKT_SZ_set','HSLB','FileName','Active','C_DC_prepdc','load_klm_calset_L1','load_klm_calset_L2','C_Target_X'])
    RCL3  = pd.merge(RCL2, HSLB,left_on='HSLB', right_on='HSLB_conf') 
    RCL4  = pd.merge(RCL3, Regions,left_on='Region', right_on='Name') 
    RCL5 = pd.DataFrame(RCL4, columns=['Name_x', 'configFolder', 'SCINT_PKT_SZ_test', 'SCINT_PKT_SZ_set','HSLB','FileName','Active','Link','Host','C_DC_prepdc','load_klm_calset_L1','load_klm_calset_L2',"C_Target_X"])
    RCL5a  = pd.merge(RCL5,C_DC_prepdc,left_on='C_DC_prepdc', right_on='Name')
    RCL5b = pd.DataFrame(RCL5a, columns=['Name_x', 'configFolder', 'SCINT_PKT_SZ_test', 'SCINT_PKT_SZ_set','HSLB','FileName','Active','Link','Host','LKBK_STRT_CVAL','LKBK_STOP_CVAL','LKBK_STRT_FVAL','LKBK_STOP_FVAL','LKBK_SCAN','load_klm_calset_L1','load_klm_calset_L2',"C_Target_X"])
    conf1 = pd.DataFrame([KLM_Conf])
    RCL6  =pd.merge(conf1, RCL5b,left_on=0, right_on='Name_x')
    C_Target_X= pd.read_excel(io=file_name, sheet_name="C_Target_X") 
    RCL7  =pd.merge(RCL6, C_Target_X,left_on="C_Target_X", right_on='Name')
    
    pd_true = pd.DataFrame([True])
    RCL7a  =pd.merge(RCL7, pd_true,left_on="Active", right_on=0)

    return RCL7a

