#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import cv2
import time

class Producer():
    """docstring for ClassName"""

    def __init__(self):
        super(Producer, self).__init__()
        # 通过cv2中的类获取视频流操作对象cap
        self.cap = cv2.VideoCapture(0)
        # 定义编码格式mpge-4
        fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', '2')
        #fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.cap.set(6, fourcc)
        self.cap.set(5, 30)  # May not implemented!
        self.cap.set(3, 640)
        self.cap.set(4, 480)

        # 调用cv2方法获取cap的视频帧（帧：每秒多少张图片）
        fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        print(fps)
        # 获取cap视频流的每帧大小
        size = (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        print(size)

        # 定义视频文件输入对象
        self.outVideo = cv2.VideoWriter('saveDir1.avi', fourcc, fps, size)

    def run(self):
        print('in producer')
        while True:
            ret, image = self.cap.read()
            if (ret == True):
                cv2.imshow('cap video', image)
                self.outVideo.write(image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.outVideo.release()
                self.cap.release()
                cv2.destroyAllWindows()
                break
                # continue

if __name__ == '__main__':
    print('run program')
    producer = Producer()
    producer.run()
