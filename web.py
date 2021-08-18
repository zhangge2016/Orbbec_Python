import os
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
    import base64
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream).decode()
    return img_stream


@app.route('/api/vis')
def hello_world():
    img_path = '/home/hogan/Googlelogo.png'
    img_stream = return_img_stream(img_path)
    return render_template('index.html',
                           img_stream=img_stream)
'''
@app.route('/api/upload', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])  # 拼接成合法文件夹地址
    file_name = '123.jpg'
    f.save(os.path.join(file_dir, file_name))  # 保存文件到upload目录
    return render_template('upload_ok.html',
                           fname=file_name)  # 向html文件以变量名fname传递参数，值为file_name对应的'123.jpg'。此处可以传递多个参数，参考附件链接

    # 传递多个参数示例 return render_template('upload_ok.html', fname = file_name, var1='aaa', var2='bbb')
'''