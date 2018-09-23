class ssh_Host:
    HostName=""
    PassWord=""
    UserName=""
    port = 22
    startCommand = ("","") #empty list of strings 
    endstring = "\n["
    IdentityFile = None