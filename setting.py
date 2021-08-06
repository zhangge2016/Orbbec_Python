
def device_info(pid):
    if pid == 1556:
        # Astra Mini
        Dwidth = 640
        Dheight = 480
        Dfps = 30
        Cwidth = 640
        Cheight = 480
        Cfps = 30
        flip = True
    elif pid == 1551:
        # Astra Plus
        Dwidth = 640
        Dheight = 480
        Dfps = 30
        Cwidth = 640
        Cheight = 480
        Cfps = 30
        flip = True
    elif pid == 1027:
        # Astra Pro
        Dwidth = 640
        Dheight = 480
        Dfps = 30
        Cwidth = 640
        Cheight = 480
        Cfps = 30
        flip = True
    elif pid == 1547:
        # Deeyea
        Dwidth = 640
        Dheight = 400
        Dfps = 30
        Cwidth = 640
        Cheight = 480
        Cfps = 30
        flip = False
    elif pid == 1031:
        # Gemini
        Dwidth = 640
        Dheight = 400
        Dfps = 30
        Cwidth = 640
        Cheight = 480
        Cfps = 30
        flip = True
    else:
        print('Please set OniDeviceInfo and parameters')
    return Dwidth, Dheight, Dfps, Cwidth, Cheight, Cfps, flip

# save start time, minute
data_save_start_time = [0, 120, 240, 360, 480, 600, 720, 840, 960, 1080, 1200, 1320]
# save interval time, microseconds
data_save_interval = 150
# save continued time for each start time, minute
data_save_continued = 60


