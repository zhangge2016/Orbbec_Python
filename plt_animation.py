import os
import cv2
import pytz
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.gridspec import GridSpec
from datetime import datetime
# (200,125) ,(300,185)
def ave_area(arrays, left_top=(350, 180), right_lower=(400,255)):
    np_array = arrays[left_top[0]:right_lower[0], left_top[1]:right_lower[1]].reshape(1, -1)
    delete_0 = np_array[np_array != 0]
    return np.mean(delete_0) / 1000

img_depths_x = []
img_depths_y = []
img_depths_x_colors = []
img_colors = []

dirs = r'Z:\12智能畜牧研究院\WeakPigDetectData\10.1.22.215\2021-09-09-18'
for file in tqdm(os.listdir(dirs)[8000:8400]):
    try:
        img_path = os.path.join(dirs, file)
        data = np.load(img_path, allow_pickle=True)
        depthPix, colorPix = data['depthPix'], data['colorPix']
        #rgbimage = cv2.cvtColor(colorPix, cv2.COLOR_BGR2RGB)
        font = cv2.FONT_HERSHEY_SIMPLEX
        text = file.replace('.npz', '')
        cv2.putText(colorPix, text, (10, 30), font, 0.75, (0, 0, 255), 2)
        cv2.putText(depthPix, text, (10, 30), font, 0.75, (0, 0, 255), 2)
        #cv2.imshow('example', colorPix)
        cv2.waitKey(10)
        indexes = file.replace('.npz', '')
        key = datetime.strptime(indexes, '%Y-%m-%d-%H-%M-%S-%f').astimezone(pytz.timezone('Asia/ShangHai')).timestamp()
        img_depths_x.append(key)
        img_depths_y.append(ave_area(depthPix))
        img_colors.append(cv2.cvtColor(colorPix,cv2.COLOR_BGR2RGB))

        depthPix = 1 - 250 / (depthPix)
        depthPix[depthPix > 1] = 1
        depthPix[depthPix < 0] = 0
        img_depths_x_colors.append(depthPix)

    except:
        print('****', file)
        continue
fig = plt.figure(dpi=100,
                 constrained_layout=True,  # 类似于tight_layout，使得各子图之间的距离自动调整【类似excel中行宽根据内容自适应】
                 figsize=(15, 12)
                 )
gs = GridSpec(3, 2, figure=fig)#GridSpec将fiure分为3行3列，每行三个axes，gs为一个matplotlib.gridspec.GridSpec对象，可灵活的切片figure
ax1 = fig.add_subplot(gs[0:2, 0:1])
ax2 = fig.add_subplot(gs[2:3, 0:2])
ax3 = fig.add_subplot(gs[0:2, 1:2])
xdata, ydata = [], []

rect = plt.Rectangle((350, 180), 75, 50, fill=False, edgecolor = 'red',linewidth=1)
ax1.add_patch(rect)
ln1 = ax1.imshow(img_colors[0])
ln2, = ax2.plot([], [], lw=2)
ln3 = ax3.imshow(img_depths_x_colors[0])
def init():
    ax2.set_xlim(img_depths_x[0], img_depths_x[-1])
    ax2.set_ylim(min(img_depths_y), max(img_depths_y))
    return ln1, ln2, ln3

def update(n):
    ln1.set_array(img_colors[n])

    xdata.append(img_depths_x[n])
    ydata.append(img_depths_y[n])
    ln2.set_data(xdata, ydata)

    ln3.set_array(img_depths_x_colors[n])

    return ln1, ln2, ln3

ani = animation.FuncAnimation(fig,
                              update,
                              frames=range(len(img_depths_x)),
                              init_func=init,
                              blit=True)
#FFwriter = animation.FFMpegWriter()
#ani.save('animation.mp4', writer = FFwriter)

ani.save('sin_dot.gif', writer='imagemagick', fps=10)
plt.show()