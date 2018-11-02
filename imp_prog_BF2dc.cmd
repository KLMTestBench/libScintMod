setMode -bs
setMode -bs
setMode -bs
setMode -bs
setCable -target "xilinx_platformusb PORT=USB21 FREQUENCY=6000000"
Identify -inferir 
identifyMPM 

assignFile -p 1 -file "/home/idlab/lastfw/concentrator_top_revo_frame9_ec6295315a4.bit"

Program -p 1 
setMode -bs
setMode -bs
deleteDevice -position 1
setMode -bs
setMode -ss
setMode -sm
setMode -hw140
setMode -spi
setMode -acecf
setMode -acempm
setMode -pff
