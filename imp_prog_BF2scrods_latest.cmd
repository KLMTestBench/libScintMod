setMode -bs 
setMode -bs 
setMode -bs 
setMode -bs 
setCable -target "digilent_plugin DEVICE=SN:210249992992 FREQUENCY=10000000" 
Identify -inferir  
identifyMPM  
assignFile -p 1 -file "/home/idlab/lastfw/181017_klmscint_simple_top.bit"
Program -p 1  
setCable -target "digilent_plugin DEVICE=SN:210249993114 FREQUENCY=10000000" 
Identify -inferir  
identifyMPM  
assignFile -p 1 -file "/home/idlab/lastfw/181017_klmscint_simple_top.bit"
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