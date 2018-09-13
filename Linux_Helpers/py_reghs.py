import re
import Linux_Helpers.shell as shell


class reghs_conf:
    filePath = "reghs" # the location of the reghs command on the computer
    link = "" # the stream location of the HSLB -abcd
    option = "fee32" 
    timeout = 1
    workingDir="/home/belle2/libScintMod/"

class py_reghs:
    def __init__(self,shell,reghs_configuration):
        self.conf = reghs_configuration
        self.shell = shell
    

    def check_return(self, commandline):
        if "=" not in commandline:
            raise Exception("Unexpected return from Commandpromt. No '=' pressent in = '" + str(commandline) +"'",commandline )
            
    def extract_number(self,commandline):
        ret = commandline.split("=")[1]
        ret=ret.splitlines()[0]
        ret = int(ret,16)
        return ret

    def call(self,key, value=None):

        
                
        if value:
            line = self.conf.filePath+ " " +self.conf.link + " " + self.conf.option + " " +key +" " +value
            self.shell.sendLine(line)
            return

        else:
            line = self.conf.filePath+ " " +self.conf.link + " " + self.conf.option + " " +key
            ret = self.shell.sendAndRecieve(line)
            self.check_return(ret)
            ret = self.extract_number(ret)
            return ret


    def stream_file(self, file):
        line = self.conf.filePath+ " " + self.conf.link + " stream " + file
        ret = self.shell.sendAndRecieve(line)
        return ret
        

    def stream_handle_return(self,ret,dummyfile, arg1,arg2,arg3,arg4,arg5,arg6,arg7,arg8,arg9,arg10,arg11,arg12):
        if "directory" in ret:
            s1="perl -e 'printf(\"%%c%%c%%c%%c%%c%%c%%c%%c%%c%%c%%c%%c\", %s,%s, %s,%s,%s,%s,%s,%s, %s,%s,%s,%s)'" %(arg1,arg2, arg3, arg4 ,arg5, arg6 ,arg7,arg8, arg9,arg10, arg11,arg12)
            s1=s1+" > " +dummyfile +" 2>&1"
            self.shell.sendLine(s1)
            ret = self.stream_file(dummyfile)
            print (ret)
            if "directory" in ret:
                raise Exception("unable to load stream file "+dummyfile)


    def stream(self, arg1,arg2,arg3,arg4,arg5,arg6,arg7,arg8,arg9,arg10,arg11,arg12):
        
        dummyfile = self.conf.workingDir + "streamfiles/test%s%s%s%s%s%s%s%s%s%s%s%s.txt" %(arg1,arg2, arg3, arg4 ,arg5, arg6 ,arg7,arg8, arg9,arg10, arg11,arg12)
        dummyfile = dummyfile.replace('0x','')
        ret = self.stream_file(dummyfile)
        self.stream_handle_return(ret,dummyfile,arg1,arg2, arg3, arg4 ,arg5, arg6 ,arg7,arg8, arg9,arg10, arg11,arg12)
        return ret
