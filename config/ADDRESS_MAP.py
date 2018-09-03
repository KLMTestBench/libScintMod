from Input_checks import range_check

class ADDRESS_MAP_CONST:
    SIZE_TOAL = 2048
    STATUS_REGISTERS = SIZE_TOAL/4
    CONTROL_REGISTERS = STATUS_REGISTERS*3

class REGISTER_ENTITY:
    def __init__(self,Index):
        self.CONTROL_START = ADDRESS_MAP_CONST.SIZE_TOAL * Index
        self.CONTROL_END   = self.CONTROL_START + ADDRESS_MAP_CONST.CONTROL_REGISTERS -1
        self.STATUS_START  = self.CONTROL_END + 1
        self.STATUS_END    = self.STATUS_START+ADDRESS_MAP_CONST.STATUS_REGISTERS-1 
        self.START_ADDR    = self.CONTROL_START
        self.END_ADDR      = self.STATUS_END

class Data_Concentrator_t(REGISTER_ENTITY):
    def __init__(self):
        REGISTER_ENTITY.__init__(self,0)
        

class RPC_Front_End_t(REGISTER_ENTITY):
    def __init__(self,Index):
        REGISTER_ENTITY.__init__(self,Index)
        range_check(Index,"RPC_Front_End_t Index",0,13)
        

class Scintillator_Mother_t(REGISTER_ENTITY):
    def __init__(self,Index):
        REGISTER_ENTITY.__init__(self,Index+13)
        range_check(Index,"Scintillator Mother Number",0,7)


Data_Concentrator = Data_Concentrator_t()

RPC_Front_End_1 = RPC_Front_End_t(1)
RPC_Front_End_2 = RPC_Front_End_t(2)
RPC_Front_End_3 = RPC_Front_End_t(3)
RPC_Front_End_4 = RPC_Front_End_t(4)
RPC_Front_End_5 = RPC_Front_End_t(5)
RPC_Front_End_6 = RPC_Front_End_t(6)
RPC_Front_End_7 = RPC_Front_End_t(7)
RPC_Front_End_8 = RPC_Front_End_t(8)
RPC_Front_End_9 = RPC_Front_End_t(9)
RPC_Front_End_10= RPC_Front_End_t(10)  
RPC_Front_End_11= RPC_Front_End_t(11)
RPC_Front_End_12= RPC_Front_End_t(12)
RPC_Front_End_13= RPC_Front_End_t(13)

Scintillator_Mother_1 = Scintillator_Mother_t(1)
Scintillator_Mother_2 = Scintillator_Mother_t(2)
Scintillator_Mother_3 = Scintillator_Mother_t(3)
Scintillator_Mother_4 = Scintillator_Mother_t(4)
Scintillator_Mother_5 = Scintillator_Mother_t(5)
Scintillator_Mother_6 = Scintillator_Mother_t(6)
Scintillator_Mother_7 = Scintillator_Mother_t(7)


