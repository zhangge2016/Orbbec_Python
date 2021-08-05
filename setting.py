
def device_info(pid):
    if pid == 1556:
        # Astra Mini
        width = 640
        height = 480
        fps = 30
    elif pid == 1551:
        # Astra Plus
        width = 640
        height = 480
        fps = 30
    elif pid == 1027:
        # Astra Pro
        width = 640
        height = 480
        fps = 30
    elif pid == 1547:
        # Deeyea
        width = 640
        height = 400
        fps = 30
    elif pid == 1031:
        # Gemini
        width = 640
        height = 400
        fps = 30
    else:
        print('Please set OniDeviceInfo and parameters')
    return width, height, fps
