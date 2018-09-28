#Adressmap of the Data Concentrator

class SFP_HSL_Aurora:
    index_0       = 0x0008
    LOOPBACK_0    = index_0
    index_1       = 0x0009
    LOOPBACK_1    = index_1
    index_2       = 0x000A
    POWERDN_2     = index_2
    index_3       = 0x000B
    POWERDN_3     = index_3
    index_4       = 0x000C
    index_5       = 0x000D
    index_6       = 0x000E
    index_7       = 0x000F
    MGTMOD0       = 0x0610 #SFP Module present
    MGTLOS        = 0x0611 #Fiber Optic Cable Connected
    TXFAULT       = 0x0612 #SFP Module fault
    HSL_LANE_UP   = 0x0613 #Aurora lane up, bit per link
    HSL_CHANNEL_UP= 0x0614 #Aurora channel up, bit per link		    SFP/HSL/Aurora
    HSL_HARD_ERR  = 0x0615 #Aurora hardware error, bit per link		SFP/HSL/Aurora
    HSL_SOFT_ERR  = 0x0616 #Aurora software error, bit per link		SFP/HSL/Aurora
    HSL_FRAME_ERR = 0x0617 #Aurora framing error, bit per link		SFP/HSL/Aurora
    TX_DST_RDY    = 0x0618 #destination ready, bit per link		    SFP/HSL/Aurora



class RPC_Parser:    
    index_0=0x0020
    index_1=0x0021
    index_2=0x0022
    index_3=0x0023
    index_4=0x0024
    index_5=0x0025
    index_6=0x0026
    index_7=0x0027

class Trigger:
    index_0=0x0028
    index_1=0x0029
    index_2=0x002A
    index_3=0x002B
    index_4=0x002C
    index_5=0x002d
    index_6=0x002E
    index_7=0x002F


class Scint_Parser_Lane_1:
    FIFO_FLAGS1 = 0x630 #Trigger/DAQ FIFO flags and errors
    TRG_PKTSZ1  = 0x631 #Trigger packet size
    DAQ_PKTSZ1  = 0x632 #DAQ packet size
    STS_PKTSZ1  = 0x633 #Status packet size

class Scint_Parser_Lane_2:
    FIFO_FLAGS2 = 0x634 #Trigger/DAQ FIFO flags and errors
    TRG_PKTSZ2  = 0x635 #Trigger packet size
    DAQ_PKTSZ2  = 0x636 #DAQ packet size
    STS_PKTSZ2  = 0x637 #Status packet size

class DAQ:
    LKBK_STRT_C   = 0x30 #1	0030	16	1	LKBK_STRT_CVAL	Lookback window course start.	High Level	DAQ
    LKBK_STOP_C   = 0x31 #2	0031	16	FF	LKBK_STOP_CVAL	Lookback window course stop.	High Level	DAQ
    LKBK_STRT_F   = 0x32 #3	0032	9	1	LKBK_STRT_FVAL	Lookback window fine start.	    High Level	DAQ 
    LKBK_STOP_F   = 0x33 #4	0033	9	FF	LKBK_STOP_FVAL	Lookback window fine stop.	    High Level	DAQ
    LKBK_SCAN     = 0x34 #5	0034	16	FFFF	LKBK_SCAN	Lookback window event trailer.	High Level	DAQ
    SCINT_SMPL_SZ = 0x35 #6	0035	8	4	SCINT_SMPL_SZ	Scintillator sample size	    High Level	DAQ
    Index_7       = 0x36 #7	0036					                                        High Level	DAQ
    Index_8       = 0x37 #8	0037					                                        High Level	DAQ

class DAQ_Path: 
    # line 2
    MISSED_TRG =0x06A0 #Missed trigger and event flags
    RPC_FLAGS  =0x06A1 #RPC event builder FIFO flags
    SCNT_FLAGS =0x06A2 #Scint. event builder FIFO flags
    RPC_TRGTAG =0x06A3 #Current RPC trigger tag
    SCNT_TRGTAG=0x06A4 #Current scint. trigger tag
    SCNT_TTERR =0x06A5 #Scint. trigger tag alignemnt error.
    RPC_DELAY  =0x06A6 #RPC front-end to event latency.
    RPC_EVTAG  =0x06A7 #Buffered RPC trigger tag.*
    SCNT_EVTAG =0x06A8 #Buffered scint trigger tag.*
    EVNT_RDCNT1=0x06A9 #Event buffer 1 read count.*
    EVNT_RDCNT2=0x06AA #Event buffer 2 read count.*
    EVNT_WRCNT1=0x06AB #Event buffer 1 write count.*
    EVNT_WRCNT2=0x06AC #Event buffer 2 write count.*
    EVNT_WDCNT =0x06AD #Number of words in event.

class Trigger_Path:
    TRG_FLAGS=0x0690 #Trigger FIFO flags.


class Run_Control:
    FIFO_FLAGS  =0x06B0 #FIFO flags
    SNUM_PKTS   =0x06B1  #Number of scint. packets
    SRC_WORDS   =0x06B2  #Number of scint. run control words
    RNUM_PKTS   =0x06B3  #Number of RPC packets
    RRC_WORDS   =0x06B4  #Last RPC run control words
    SCINT_PKT_SZ=0x0038 
    RPC_PKT_SZ  =0x0039


#Some of the registers are permanently monitored by a script 'dcregs.sh', which is located on
class dcregs(Scint_Parser_Lane_1, Scint_Parser_Lane_2, DAQ_Path): #
    HSL_CHAN_UP = SFP_HSL_Aurora.HSL_CHANNEL_UP
    LKBK_STRT_C = DAQ.LKBK_STRT_C
    LKBK_STOP_C = DAQ.LKBK_STOP_C
    LKBK_STRT_F = DAQ.LKBK_STRT_F
    LKBK_STOP_F = DAQ.LKBK_STOP_F

class ftsw_register:
    trigger_limiter = '0x9f0'
    lookBackWindow =  '0x9e0'