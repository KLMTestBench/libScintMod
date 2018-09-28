import pandas as pd

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from config.config_make_default_connections import config_make_default_connections

def load_known_hosts(file_name):
    Known_hosts = pd.read_excel(io=file_name, sheet_name="Known_hosts")
    config_make_default_connections(Known_hosts)
    return Known_hosts