#!/usr/bin/env python3

from datetime import datetime
import argparse
import platform
import os
import re
from openni import openni2
from openni import _openni2 as c_api
import cv2
import numpy as np
import setting


def getOrbbec():
    # 记载 openni
    try:
        platforms = platform.platform()
        if re.search('Windows', platforms):
            libpath = "lib/Windows"
        elif re.search('armv7l', platforms):
            libpath = "lib/ARM32"
        elif re.search('aarch64', platforms):
            libpath = "lib/ARM64"
        else:
            print("ERROR OpenNI2 lib loaded, maybe download x86_64 type\n")
        print("library path is: ", os.path.join(os.path.dirname(__file__), libpath))
        openni2.initialize(os.path.join(os.path.dirname(__file__), libpath))
        print("OpenNI2 initialized \n")
    except Exception as ex:
        print("ERROR OpenNI2 not initialized", ex, " check library path..\n")
        return

    # 加载 orbbec 相机
    try:
        device = openni2.Device.open_any()
        OniDeviceInfo = device.get_device_info()
        return device, OniDeviceInfo
    except Exception as ex:
        print("ERROR Unable to open the device: ", ex, " device disconnected? \n")
        return

def parse_args():
    '''PARAMETERS'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--interval', type=int, default=150, help='save interval microseconds')
    parser.add_argument('--mirroring', default=True, help='mirroring [default: False]')
    parser.add_argument('--compression', default=True, help='compress or not, when saving the video [default: True]')
    parser.add_argument('--outdir', default='D:/test', help='dir of save .npy')
    parser.add_argument('--getDataType', default=True)
    parser.add_argument('--visDataType', default=True)

    return parser.parse_args()

def get_depth_stream(device, width, height, fps):
    depth_stream = device.create_depth_stream()
    depth_stream.set_mirroring_enabled(args.mirroring)
    depth_stream.start()
    try:
        depth_stream.set_video_mode(c_api.OniVideoMode(resolutionX=width, resolutionY=height, fps=fps,
                                                       pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_100_UM))
    except:
        pass
    return depth_stream

def get_color_stream(device, width, height, fps, uvc=True):
    if uvc == True:
        color_stream = cv2.VideoCapture(0)
    else:
        color_stream = device.create_color_stream()
        color_stream.start()
        try:
            color_stream.set_video_mode(c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888,
                                                           resolutionX=width, resolutionY=height, fps=fps))
        except:
            pass
    return color_stream


def get_depth_data(depth_stream, height, width):

    # 5s未能获取数据，中断程序
    if openni2.wait_for_any_stream([depth_stream], 5) is None:
        raise

    frame_depth = depth_stream.read_frame()
    frame_depth_data = frame_depth.get_buffer_as_uint16()
    # 读取帧的深度信息 depth_array 也是可以用在后端处理的 numpy格式的
    depthPix = np.frombuffer(frame_depth_data, dtype=np.uint16)
    depthPix = np.ndarray((height, width), dtype=np.uint16, buffer=depthPix)

    return depthPix


def get_color_data(color_stream, width, height, uvc=True, flip=True):
    if uvc == True:
        _, color_array = color_stream.read()
        if flip == True:
            colorPix = cv2.flip(color_array, 1)
        else:
            colorPix = color_array
    else:
        frame_color = color_stream.read_frame()
        frame_data = frame_color.get_buffer_as_uint8()
        colorPix = np.frombuffer(frame_data, dtype=np.uint8)
        colorPix.shape = (height, width, 3)
        if flip == True:
            colorPix = np.flip(colorPix, 2)
        else:
            colorPix = colorPix

    return colorPix

def getData(args, uvc):
    device, OniDeviceInfo = getOrbbec()
    print(OniDeviceInfo, OniDeviceInfo.usbProductId)
    Dwidth, Dheight, Dfps, Cwidth, Cheight, Cfps, flip = setting.device_info(pid=OniDeviceInfo.usbProductId)

    # 创建深度流
    depth_stream = get_depth_stream(device=device, width=Dwidth, height=Dheight, fps=Dfps)
    # 创建rgb流
    color_stream = get_color_stream(device=device, width=Cwidth, height=Cheight, fps=Cfps, uvc=uvc)

    # 设置 镜像 帧同步
    device.set_image_registration_mode(c_api.OniImageRegistrationMode.ONI_IMAGE_REGISTRATION_DEPTH_TO_COLOR)
    device.set_depth_color_sync_enabled(True)

    while True:
        # 读取帧
        depthPix = get_depth_data(depth_stream=depth_stream, height=Dheight, width=Dwidth)

        # 读取 彩色图
        colorPix = get_color_data(color_stream=color_stream, height=Cheight, width=Cwidth, uvc=uvc, flip=flip)
        #print(np.shape(depthPix), np.shape(colorPix))
        if args.getDataType:
            filename = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f') + '.npz'
            if not os.path.exists(args.outdir):
                os.mkdir(args.outdir)
            np.savez(os.path.join(args.outdir, filename), depthPix=np.array(depthPix), colorPix=np.array(colorPix))
            #print("save %s done" % filename)

        if args.visDataType:
            # 变换格式用于 opencv 显示

            depthPix = 1 - 250 / (depthPix)
            depthPix[depthPix > 1] = 1
            depthPix[depthPix < 0] = 0
            '''
            depthPix.shape = (1, setting.height, setting.width)
            depthPix = np.concatenate((depthPix, depthPix, depthPix), axis=0)
            depthPix = np.swapaxes(depthPix, 0, 2)
            depthPix = np.swapaxes(depthPix, 0, 1)
            depthPix = depthPix.astype(np.uint8)  # This is required to be able to draw it  # This is required to be able to draw it
            '''
            cv2.imshow('depth', depthPix)
            cv2.imshow('color', colorPix)
        # 时间间隔
        key_value = cv2.waitKey(args.interval)  # 捕获键值
        # 键盘监听
        if key_value & 0xFF == ord(' '):  # 空格键实现暂停与开始
            cv2.waitKey(0)
        elif key_value & 0xFF == ord('q'):  # ‘q’键实现退出
            # 关闭窗口 和 相机
            depth_stream.stop()
            try:
                color_stream.release()
                cv2.destroyAllWindows()
            except:
                color_stream.stop()
            break

    # 检测设备是否关闭（没什么用）
    try:
        openni2.unload()
        print("Device unloaded \n")
    except Exception as ex:
        print("Device not unloaded: ", ex, "\n")


if __name__ == '__main__':
    args = parse_args()
    cap = cv2.VideoCapture(0)

    if cap is None or not cap.isOpened():
        uvc = False
    else:
        uvc = True
    cap.release()
    getData(args=args, uvc=uvc)


