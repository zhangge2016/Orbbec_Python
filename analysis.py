"""
import argparse
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, find_peaks


def parse_args():
    '''PARAMETERS'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--time_start', default=True, help='mirroring [default: False]')
    parser.add_argument('--interval', default=True, help='compress or not, when saving the video [default: True]')
    parser.add_argument('--axis', default='/data', help='dir of save .npy')

    return parser.parse_args()


def ave_area(arrays, left_top=(330,210), right_lower=(350,240)):
    np_array = arrays[left_top[0]:right_lower[0], left_top[1]:right_lower[1]].reshape(1, -1)
    delete_0 = np_array[np_array != 0]
    return np.mean(delete_0) / 100

def moving_average(interval, windowsize):
    window = np.ones(int(windowsize)) / float(windowsize)
    print('*',window)
    re = np.convolve(interval, window, 'valid')
    return re

x_axis_data = []
y_axis_data = []
for i, arr in enumerate(arrays):
    ave_value = ave_area(arr)
    y_axis_data.append(ave_value)
    x_axis_data.append(i*250)
fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1)  # 3行3列的第一个位置
ax2 = fig.add_subplot(2, 1, 2)  # 3行3列的第一个位置
ax1.plot(x_axis_data, y_axis_data, 'ro-', color='#4169E1', alpha=0.4, linewidth=1)

#y_av = moving_average(y_axis_data, 4)
y_av = savgol_filter(y_axis_data, 7, 3, mode='nearest')
print(len(x_axis_data), len(y_av))
ax2.plot(x_axis_data, y_av, 'ro-', color='#9370DB', alpha=0.4, linewidth=1)

def callpeak(x):

    peaks, properties = find_peaks(x, prominence=0)#, width=4)
    print(peaks)
    print(properties)
    # Output
    return peaks

peaks = callpeak(x=y_axis_data)
peak_x = []
peak_y = []
colors = '#DC143C'
area = np.pi * 4**2  # 点面积
for index in peaks:
    peak_x.append(index*250)
    peak_y.append(y_axis_data[index])
ax1.scatter(peak_x, peak_y, s=area, c=colors, alpha=0.8)

peaks = callpeak(x=y_av)
peak_x = []
peak_y = []
colors = '#DC143C'
area = np.pi * 4**2  # 点面积
for index in peaks:
    peak_x.append(index*250)
    peak_y.append(y_av[index])
ax2.scatter(peak_x, peak_y, s=area, c=colors, alpha=0.8)
plt.show()
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'ro')

def init():
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-1, 1)
    return ln,

def update(frame):
    xdata.append(frame)
    ydata.append(np.sin(frame))
    ln.set_data(xdata, ydata)
    return ln,

ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
                    init_func=init, blit=True)
ani.save('sin_dot.gif', writer='imagemagick', fps=30)

plt.show()

