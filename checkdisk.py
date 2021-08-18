# coding:utf-8
import os
import sys
import signal
import psutil
import subprocess

from apscheduler.schedulers.blocking import BlockingScheduler

def checkprocess(processname):
    '''
    列出所有当前正在运行的进程pid-cmdline信息
    :param processname:
    :return:
    '''
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'cmdline'])
        except psutil.NoSuchProcess:
            pass
        else:
            if processname in pinfo['cmdline']:
                return pinfo['pid']

def spaceMonitorJob():
    '''
    当磁盘(切片存储的目录)利用率超过90%,程序退出
    :return:
    '''
    try:
        st = psutil.disk_usage('/data')
        used_percent = st.percent
    except FileNotFoundError:
        print('check webroot space error.')

        # 移除任务，病关闭sched任务
        sched.remove_job(job_id='id_space_monitor')
        sched.shutdown(wait=False)
        sys.exit(-3)
    main_pid = checkprocess("scheduler.py")
    if isinstance(main_pid, int):
        print("进程存在")
        if used_percent > 90:
            print('No enough space.')
            sched.remove_job(job_id='id_space_monitor')
            sched.shutdown(wait=False)
            # 杀掉进程
            os.killpg(main_pid, signal.SIGKILL)
            # 退出
            sys.exit(-3)
        else:
            pass
    else:
        print("进程不存在")
        if used_percent > 90:
            print('No enough space.')
            sched.remove_job(job_id='id_space_monitor')
            sched.shutdown(wait=False)
            # 退出
            sys.exit(-3)
        else:
            # zora P1开发板用户切换有密码，采用subprocess模块（通过修改系统配置免密也可使用os模块调用）
            cmd = 'su - root -c "python3 /home/orbbec/Downloads/Orbbec_Python-main/scheduler.py"'
            p = subprocess.Popen(cmd, shell = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE)
            password = 'orbbec'
            p.stdin.write(password.encode('utf-8'))
            # raspberry Pi开发板默认免密，可以直接使用os模块
            #os.system('nohup python3 /home/pi/Downloads/Orbbec_python-main/scheduler.py &')


# 开启磁盘空间检测
sched = BlockingScheduler(timezone='Asia/Shanghai')

# 给检查任务设个id,方便任务的取消
sched.add_job(spaceMonitorJob, 'interval', id='id_space_monitor', minutes=1)

sched.start()
