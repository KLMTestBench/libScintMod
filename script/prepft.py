class prepft_conf:
    devices = ""
    lookBackWindow = 0x0
    TL_NumberOfTrigger = 0
    TL_timeInMicroSeconds = 0
    use_EKLM = False

def prepft(ftsw,config=prepft_conf()):
    ret = ""
    ret += ftsw.reset()
    ret += ftsw.set_trigger_limiter(config.TL_NumberOfTrigger,config.TL_timeInMicroSeconds)
    ret += ftsw.set_lookBackWindow(config.lookBackWindow)
    ret += ftsw.utime()
    ret += ftsw.reset_ttaddr(config.use_EKLM)
    ret += ftsw.prepare_devices(config.devices,config.use_EKLM)
    ret += ftsw.reset()
    return ret