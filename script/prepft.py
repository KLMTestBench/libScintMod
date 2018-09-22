class prepft_conf:
    devices = ""
    lookBackWindow = 0x0
    TL_NumberOfTrigger = 0
    TL_timeInMicroSeconds = 0
    use_EKLM = False

def prepft(ftsw,config=prepft_conf()):
    print(ftsw.reset())
    print(ftsw.set_trigger_limiter(config.TL_NumberOfTrigger,config.TL_timeInMicroSeconds))
    print(ftsw.set_lookBackWindow(config.lookBackWindow))
    print(ftsw.utime())
    print(ftsw.reset_ttaddr(config.use_EKLM))
    print(ftsw.prepare_devices(config.devices,config.use_EKLM))
    print(ftsw.reset())