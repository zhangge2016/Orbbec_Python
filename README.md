
  Support ARM32/ARM64/Window system
  
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
      
      添加export OPENBLAS_CORETYPE=ARMV8至/etc/profile
      
      source /etc/profile
      
      reboot