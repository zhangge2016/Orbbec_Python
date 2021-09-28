import paramiko
import re
import os
import threading
import math
import time


class SSHConnection:
    # 初始化连接创建Transport通道
    def __init__(self, host='xxx.xxx.xxx.xxx', port=22, user='xxx', pwd='xxxxx'):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.__transport = paramiko.Transport((self.host, self.port))
        self.__transport.connect(username=self.user, password=self.pwd)
        self.sftp = paramiko.SFTPClient.from_transport(self.__transport)

    # 关闭通道
    def close(self):
        self.sftp.close()
        self.__transport.close()

    # 上传文件到远程主机
    def upload(self, local_path, remote_path):
        self.sftp.put(local_path, remote_path)

    # 从远程主机下载文件到本地
    def download(self, local_path, remote_path):
        self.sftp.get(remote_path, local_path)

    # 在远程主机上创建目录
    def mkdir(self, target_path, mode='0777'):
        self.sftp.mkdir(target_path, mode)

    # 删除远程主机上的目录
    def rmdir(self, target_path):
        self.sftp.rmdir(target_path)

    # 查看目录下文件以及子目录（如果需要更加细粒度的文件信息建议使用listdir_attr）
    def listdir(self, target_path):
        return self.sftp.listdir(target_path)

    # 删除文件
    def remove(self, target_path):
        self.sftp.remove(target_path)

    # 查看目录下文件以及子目录的详细信息（包含内容和参考os.stat返回一个FSTPAttributes对象，对象的具体属性请用__dict__查看）
    def listdirattr(self, target_path):
        try:
            list = self.sftp.listdir_attr(target_path)
        except BaseException as e:
            print(e)
        return list

    # 获取文件详情
    def stat(self, remote_path):
        return self.sftp.stat(remote_path)

    # SSHClient输入命令远程操作主机
    def cmd(self, command):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh._transport = self.__transport
        stdin, stdout, stderr = ssh.exec_command(command)
        result = stdout.read().decode()
        return result

def thread_(rootdir, host, files):
    p = SSHConnection(host='10.1.22.21', user='root', pwd='orbbec')
    for file in files:
        remote_path = '/data/' + rootdir + '/' + file
        local_path = 'Z:/WeakPigDetectData/' + host + '/' + rootdir + '/' + file
        # _thread.start_new_thread(p.download, (local_path, remote_path))
        # print(remote_path,local_path)
        p.download(remote_path=remote_path, local_path=local_path)
host = '10.1.22.21'
user = 'root'
pwd = 'orbbec'
p = SSHConnection(host='10.1.22.21', user='root', pwd='orbbec')
while True:
    rootdir_str = p.cmd(command='ls -t /data')
    rootdir_list = re.split('\n', rootdir_str)[:-1]
    print(rootdir_list)
    if len(rootdir_list) >= 2:
        print(list(reversed(rootdir_list[1:])))
        for rootdir in list(reversed(rootdir_list[1:])):
            print(rootdir)
            if os.path.exists('Z:/WeakPigDetectData/' + host + '/' + rootdir):
                pass
            else:
                os.makedirs('Z:/WeakPigDetectData/' + host + '/' + rootdir)
            #try:
            files = p.listdir('/data/' + rootdir)
            num = math.ceil(len(files)/5)
            threads = []
            for i in range(5):
                # 创建多线程
                t = threading.Thread(target=thread_, args=(rootdir, host, files[i*num:(i+1)*num]))
                threads.append(t)
            for i in range(5):
                # 启用多线程
                threads[i].start()
            '''
            for file in tqdm(files):
                remote_path = '/data/' + rootdir + '/' + file
                local_path = 'Z://WeakPigDetectData/' + host + '/' + rootdir + '/' + file
                #_thread.start_new_thread(p.download, (local_path, remote_path))
                #print(remote_path,local_path)
                p.download(remote_path=remote_path, local_path=local_path)
                # time.sleep(0.5)
            '''
            remote_num = len(files)
            local_num = len(os.listdir('Z:/WeakPigDetectData/' + host + '/' + rootdir))
            while remote_num != local_num:
                print('%s Dowload uncompleted: %s/%s\n' % (host + '/' + rootdir, local_num, remote_num))
                time.sleep(10)
                remote_num = len(files)
                local_num = len(os.listdir('Z:/WeakPigDetectData/' + host + '/' + rootdir))

            if remote_num == local_num:
                p.cmd(command='rm -rf /data/%s' % rootdir)
                print('%s Dowload completed: %s/%s\n' % (host + '/' + rootdir, local_num, remote_num))
            else:
                print('%s Dowload uncompleted: %s/%s\n' % (host + '/' + rootdir, local_num, remote_num))
            #except:
            #   print('%s Dowload failed\n' % (host + '/' + rootdir))
            #    #continue
    p.close()
