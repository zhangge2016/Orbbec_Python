# coding:utf-8
import os
import cv2
import base64
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template, request

# 设置了静态目录为./upload_pics，方便传递参数给html文件之后，显示图片
# 假设上述目录下有一张123.jpg图片文件
# 本例为了演示和方便理解，略去了传图片时的校验代码

app = Flask(__name__, static_folder='./upload_pics')

UPLOAD_FOLDER = 'upload_pics'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # 设置文件上传的目标文件夹

basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前项目的绝对路径


def return_img_stream(img_local_path):
    """
    工具函数:
    获取本地图片流
    :param img_local_path:文件单张图片的本地绝对路径
    :return: 图片流
    """
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()

        img_stream = base64.b64encode(img_stream).decode()
    return img_stream

def get_recent_data():
    root = r'D:\data'
    if os.listdir(root) != []:
        root_dicts = {int(x.replace('-', '')): x for x in os.listdir(root)}
        root_recent = sorted(root_dicts.keys(), reverse=True)[0]
        rootdir = os.path.join(root, root_dicts[root_recent])
        if os.listdir(rootdir) != []:
            recent_dicts = {int(x.replace('-', '').replace('.npz', '')): x for x in os.listdir(rootdir)}
            recent_ms = sorted(recent_dicts.keys(), reverse=True)[0]
            img_path = os.path.join(rootdir, recent_dicts[recent_ms])
            data = np.load(img_path, allow_pickle=True)
            depthPix, colorPix = data['depthPix'], data['colorPix']
            depthPix_flatten = [x for x in depthPix.flatten(order='C') if x !=0]

            depthPix = 1 - 250 / (depthPix)
            depthPix[depthPix > 1] = 1
            depthPix[depthPix < 0] = 0
            depthPix = depthPix*255

            font = cv2.FONT_HERSHEY_SIMPLEX
            text = recent_dicts[recent_ms].replace('.npz', '')
            cv2.putText(colorPix, text, (10, 30), font, 0.75, (0, 0, 255), 2)
            cv2.putText(depthPix, text, (10, 30), font, 0.75, (0, 0, 255), 2)
            cv2.imwrite('images/depth.png', depthPix)
            cv2.imwrite('images/color.png', colorPix)

            plt.hist(depthPix_flatten, bins=200, color='red', histtype='stepfilled', alpha=0.75)
            plt.title('Distance distribution')
            plt.xlabel('distance')
            plt.ylabel('number')
            plt.savefig('images/hist.png')
            plt.close()
            return 1
        else:
            return 0
    else:
        return 0

@app.route('/api/vis')
def hello_world():
    code = get_recent_data()
    if code == 1:
        depth_stream = return_img_stream('images/depth.png')
        color_stream = return_img_stream('images/color.png')
        hist_stream = return_img_stream('images/hist.png')
        return render_template('vis_index.html',
                               depth_stream=depth_stream,
                               color_stream=color_stream,
                               hist_stream=hist_stream)
    else:
        init_stream = return_img_stream('images/init.png')
        return render_template('vis_index.html',
                               depth_stream=init_stream,
                               color_stream=init_stream,
                               hist_stream=init_stream)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False, use_reloader=False)