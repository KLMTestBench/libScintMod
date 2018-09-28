import time
base_path ="/home/group/b2klm/run/scripts/"
from threading import Thread, Lock

def load_klm_calset(shell_factory,RCL,Parallel=False):
    local_Threads = []
    ret = ''
    for i in range(len(RCL.index)):
        e = RCL.iloc[i]
        host = str(e.Host)
        lineL1, lineL2 =  create_line(e)
        #print(lineL1)
        #print(lineL2)
        if Parallel:
            t = Thread(target = do_calset, args = (shell_factory,lineL1,host,ret))
            t.start()
            local_Threads.append(t)
            time.sleep(1)
            
            t = Thread(target = do_calset, args = (shell_factory,lineL2,host,ret))
            t.start()
            local_Threads.append(t)
            time.sleep(1)
        else:
            do_calset(shell_factory,lineL1,host,ret)
            do_calset(shell_factory,lineL2,host,ret)

    
    for x in local_Threads:
        x.join()

        


def create_line(e):
    CalSet_Folder_L1 = e.CalSet_Folder_L1
    CalSet_Folder_L2 = e.CalSet_Folder_L2
    th = int(e.Threshold)
    load_klm_calset_L1 = e.load_klm_calset_L1
    load_klm_calset_L2 = e.load_klm_calset_L2
    lineL1 = base_path + CalSet_Folder_L1 + "/"+load_klm_calset_L1 +'.sh  ' + str(th)
    lineL2 = base_path + CalSet_Folder_L2 + "/"+load_klm_calset_L2 +'.sh  ' + str(th)

    return lineL1,lineL2


def do_calset(shell_factory,line,host,ret):
    sucess = False
    for _ in range(10):
        if sucess:
            print("done "+ line)
            return

        try:
            print(line)
            ret = shell_factory.run_on(host,line)
            print(ret)
            sucess = True
        except:
            print("fail " + line)
        

