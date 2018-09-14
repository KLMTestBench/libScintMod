roi = [
('HSL_CHANNEL_UP',1556),
('FIFO_FLAGS1',1584),
('DAQ_PKTSZ1',1586),
('FIFO_FLAGS2',1588),
('DAQ_PKTSZ2',1590),
('MISSED_TRG',1696),
('SCINT_FLAGS',1698),
('SCINT_TRGTAG',1700),
('SCINT_EVTAG',1704),
('EVNT_RDCNT1',1705),
('EVNT_RDCNT2',1706),
('EVNT_WRCNT1',1707),
('EVNT_WRCNT2',1708),
('EVNT_WDCNT',1709)
]

def visualise_ROIs(hslb,roi,sample):
    line0=''
    line1='\t '
    i = 0
    for name,var in roi:
        i+=1
        if i%2 == 0:
            line0 += name + "\t "
        else:
            line1 += name + "\t "
    
    print(line0)
    print(line1)
    for _ in range(3):
        line =''
        for name,var in roi:
            line += str(hslb.reghs(var)) +'\t '
        print(line)