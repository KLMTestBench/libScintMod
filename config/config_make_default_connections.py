
import math

def config_make_default_connections(config,MainIndex=0,DefaultIndex=1):
    for i in range(len(config.index)):
        x = config.iat[i,MainIndex]
        make_connection(config,x,MainIndex,DefaultIndex)


def get_index_by_name(config,ConfigName,MainIndex=0):
    for i in range(len(config.index)):
        if config.iat[i,MainIndex] == ConfigName:
            return i
    
    raise Exception("unable to find element",ConfigName)

def make_connection(config,ConfigName,MainIndex=0,DefaultIndex=1):
    #print(ConfigName)
    i=get_index_by_name(config,ConfigName,MainIndex)
    default = config.iat[i,DefaultIndex]
    #print(default)
    if isinstance(default,str):
        #print(x)
        default_index = make_connection(config,default,MainIndex,DefaultIndex)
        config_fill_default(config,i,default_index)
        #print(x)
    
    return i






def config_fill_default(config, x,default):
    c = list(config)
    for c1 in range(len(c)):
        e = config.iat[x,c1]  
        if not(isinstance(e,str) or not math.isnan(e)):
            config.iat[x,c1] = config.iat[default,c1]
    return x