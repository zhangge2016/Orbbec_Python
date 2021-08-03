#!/usr/bin/env python3

from datetime import datetime
import argparse
import sys
import os
import time
from openni import openni2
from openni import _openni2 as c_api
import cv2
import numpy as np


def getOrbbec():
    # 记载 openni
    try:
        if sys.platform == "win32":
            libpath = "lib/Windows"
        else:
            libpath = "lib/Linux"
        print("library path is: ", os.path.join(os.path.dirname(__file__), libpath))
        openni2.initialize(os.path.join(os.path.dirname(__file__), libpath))
        print("OpenNI2 initialized \n")
    except Exception as ex:
        print("ERROR OpenNI2 not initialized", ex, " check library path..\n")
        return

    # 加载 orbbec 相机
    try:
        device = openni2.Device.open_any()
        return device
    except Exception as ex:
        print("ERROR Unable to open the device: ", ex, " device disconnected? \n")
        return

def parse_args():
    '''PARAMETERS'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', type=int, default=640, help='resolutionX')
    parser.add_argument('--height', type=int, default=480, help='resolutionY')
    parser.add_argument('--fps', type=int, default=1, help='frame per second')
    parser.add_argument('--mirroring', default=True, help='mirroring [default: False]')
    parser.add_argument('--compression', default=True, help='compress or not, when saving the video [default: True]')
    parser.add_argument('--outdir', help='dir of save .npy')
    parser.add_argument('--start_time', help='minute, 2：00 is 120, eg.[120, 600]')
    parser.add_argument('--interval', type=int, default=150, help='save interval microseconds')
    parser.add_argument('--time_long', type=int, default=3, help='minute')




    return parser.parse_args()


def getData(args, minute_ok_lists):
    device = getOrbbec()
    # 创建深度流

    depth_stream = device.create_depth_stream()
    depth_stream.set_mirroring_enabled(args.mirroring)
    depth_stream.set_video_mode(c_api.OniVideoMode(resolutionX=args.width, resolutionY=args.height, fps=args.fps,
                                                   pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM))

    # 获取uvc
    cap = cv2.VideoCapture(0)

    # 设置 镜像 帧同步
    device.set_image_registration_mode(c_api.OniImageRegistrationMode.ONI_IMAGE_REGISTRATION_DEPTH_TO_COLOR)
    device.set_depth_color_sync_enabled(True)
    depth_stream.start()


    while True:
        time_now = datetime.now()
        minutes_ = int(time_now.hour) * 60 + int(time_now.minute)
        if minutes_ in minute_ok_lists:
            # 读取帧
            frame_depth = depth_stream.read_frame()
            frame_depth_data = frame_depth.get_buffer_as_uint16()
            # 读取帧的深度信息 depth_array 也是可以用在后端处理的 numpy格式的
            depthPix = np.frombuffer(frame_depth_data, dtype=np.uint16)

            # 读取 彩色图
            _, color_array = cap.read()
            color_flip = cv2.flip(color_array, 1)

            filename = time_now.strftime('%Y-%m-%d-%H-%M-%S-%f') + '.npy'
            if not os.path.exists(args.outdir):
                os.mkdir(args.outdir)
            arr = np.array([depthPix, color_flip])
            np.save(os.path.join(args.outdir, filename), arr)
            print("save %s done" % filename)
        else:
            # 关闭窗口 和 相机
            depth_stream.stop()
            cap.release()
            cv2.destroyAllWindows()
            break
        key_value = cv2.waitKey(args.interval)  # 捕获键值

    '''
    # 检测设备是否关闭（没什么用）
    try:
        openni2.unload()
        print("Device unloaded \n")
    except Exception as ex:
        print("Device not unloaded: ", ex, "\n")
    '''

if __name__ == '__main__':
    args = parse_args()
    minute_ok_lists = []
    for i in eval(args.start_time):
        minute_ok_lists = list(range(i, i + args.time_long))
        time_now = datetime.now()
        minutes_ = int(time_now.hour) * 60 + int(time_now.minute)
        print(minutes_, minute_ok_lists)
        while minutes_ not in minute_ok_lists:
            time.sleep(1)
            time_now = datetime.now()
            minutes_ = int(time_now.hour) * 60 + int(time_now.minute)
        getData(args, minute_ok_lists)
