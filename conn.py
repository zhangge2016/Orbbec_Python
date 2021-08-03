#!/usr/bin/env python3

from datetime import datetime
import argparse
import sys
import os
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
    parser.add_argument('--interval', type=int, default=150, help='save interval microseconds')
    parser.add_argument('--mirroring', default=True, help='mirroring [default: False]')
    parser.add_argument('--compression', default=True, help='compress or not, when saving the video [default: True]')
    parser.add_argument('--mode', default='VIEWER', help='viewer or not')
    parser.add_argument('--outdir', help='dir of save .npy')
    parser.add_argument('--getDataType', default=False)
    parser.add_argument('--visDataType', default=True)


    return parser.parse_args()


def getData(args):
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
        # 读取帧
        frame_depth = depth_stream.read_frame()
        frame_depth_data = frame_depth.get_buffer_as_uint16()
        # 读取帧的深度信息 depth_array 也是可以用在后端处理的 numpy格式的
        depthPix = np.frombuffer(frame_depth_data, dtype=np.uint16)

        # 读取 彩色图
        _, color_array = cap.read()
        color_flip = cv2.flip(color_array, 1)
        if args.getDataType:
            filename = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f') + '.npy'
            if not os.path.exists(args.outdir):
                os.mkdir(args.outdir)
            arr = np.array([depthPix, color_flip])
            np.save(os.path.join(args.outdir, filename), arr)
            print("save %s done" % filename)

        if args.visDataType:
            # 变换格式用于 opencv 显示
            depthPix = np.ndarray((args.height, args.width), dtype=np.uint16, buffer=frame_depth_data)
            depthPix = 1 - 250 / (depthPix)
            depthPix[depthPix > 1] = 1
            depthPix[depthPix < 0] = 0
            '''
            depthPix.shape = (1, args.height, args.width)
            depthPix = np.concatenate((depthPix, depthPix, depthPix), axis=0)
            depthPix = np.swapaxes(depthPix, 0, 2)
            depthPix = np.swapaxes(depthPix, 0, 1)
            depthPix = depthPix.astype(np.uint8)  # This is required to be able to draw it  # This is required to be able to draw it
            '''
            print(np.shape(depthPix), np.shape(color_flip))
            cv2.imshow('depth', depthPix)
            cv2.imshow('color', color_flip)
        # 时间间隔
        key_value = cv2.waitKey(args.interval)  # 捕获键值
        # 键盘监听
        if key_value & 0xFF == ord(' '):  # 空格键实现暂停与开始
            cv2.waitKey(0)
        elif key_value & 0xFF == ord('q'):  # ‘q’键实现退出
            # 关闭窗口 和 相机
            depth_stream.stop()
            cap.release()
            cv2.destroyAllWindows()
            break

    # 检测设备是否关闭（没什么用）
    try:
        openni2.unload()
        print("Device unloaded \n")
    except Exception as ex:
        print("Device not unloaded: ", ex, "\n")


if __name__ == '__main__':
    args = parse_args()
    getData(args)

