
  Support ARM32/ARM64/Window system
  
  python安装包：
  
    openni==2.3.0
    opencv-python==4.5.3.56
    apscheduler==3.7.0
    flask==2.0.1
    matplotlib==2.1.1
    psutil==5.8.0
    numpy==1.19.4
  
  1、Zora P1 开发板
      
    1）Ubuntu 烧录
      
      烧录工具下载：USB_Burning_Tool（下载：https://abzg-oss.oss-cn-shenzhen.aliyuncs.com/files/Setup_Aml_Burn_Tool_v2.2.3.3.exe）
      
      Ubuntu系统固件下载：https://developer-orbbec-oss.oss-cn-shenzhen.aliyuncs.com/files/Orbbec_Ubuntu1804_Zora-P1_20210712.rar
      
      烧录教程：https://developer.orbbec.com.cn/technical_library.html
      
    2）Python3环境配置（自带python3.6和python2.7）
          
          sudo apt-get install python3-pip
          
          python3 -m pip install scikit-build
          
          python3 -m pip install --upgrade pip setuptools wheel
          
          sudo python3 -m pip install openni opencv-python
          
    3)Illegal instruction错误
      
      添加export OPENBLAS_CORETYPE=ARMV8至~/.bashrc
      
      source ~/.bashrc
  
  2、Raspberry Pi 4开发板
  
    1）Ubuntu 烧录
      
      烧录工具下载：Raspberry Pi Imager（下载：https://downloads.raspberrypi.org/imager/imager_1.6.2.exe）
      
      Ubuntu系统固件下载：2021-03-04-raspios-buster-armhf-full.zip（32位desktop版本）
      
      烧录教程：https://ubuntu.com/tutorials/how-to-install-ubuntu-desktop-on-raspberry-pi-4#2-prepare-the-sd-card
      
    2）Python3环境配置（自带python3.7和python2.7）
                    
          sudo apt-get install libatlas-base-dev
          
          sudo apt-get install python3-opencv
          
          python3 -m pip install openni
          
  3、RK3399 pro 开发板
  
    1）Ubuntu 烧录
  
    烧录工具下载：AndroidTool_Release_v2.65（下载：https://download.t-firefly.com/product/Board/RK3399Pro/Tool/Windows/AndroidTool/AndroidTool_Release_v2.65.rar）
    
    Ubuntu系统固件下载：AIO-RK3399PRO-JD4-Ubuntu_18.04.5_LTS_DESKTOP_PYTHON3.5-RKNN-OPENCV-20210413-1746.img.7z
    
    烧录教程：下载的烧录工具包中《Android开发工具手册_v1.2.pdf》文件
    
    2）Python3环境配置（自带python3.6、python3.5和python2.7，建议使用3.6版本）
                    
          pip3 install opencv-python
          
          pip3 install openni