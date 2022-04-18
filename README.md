# dis-os


## 项目地址

**github**：https://github.com/ro-ken/dis-os

**gitee**：https://gitee.com/ro_ken/dis-os


## 目录结构

- dataset：数据集

- app：任务模型

- module:一些独立的模块
   
  - group：小组成员的个人的文件（无关）
  - node_helper：

    - node_handler.py：节点的辅助类，一些业务函数封装在里面
    - node_struct.py：节点的一些数据结构
  
  - proto：grpc的接口文件（自己生成）
  - sched：节点的任务调度器

    - sched.py：调度器接口，具体的调度类要继承这个接口类
    - sched_api.py：供上层函数选择用哪个接口
  
  - task_helper:client、server的辅助类
     
    - client_handler.py：client_handler的辅助类，一些业务函数
    - task_handler.py:grpc接口在client端的函数
    - task_service.py:grpc接口在server端的实现
- tools

    - requirements.txt:需要的依赖
    - utils.py:通用的方法
    - io_utils.py:文件IO通用的方法
    - random_num.py：生成随机数的文件

- settings.py：主配置文件
- node.py启动项目
- client_node.py:client线程
- server_node.py:server线程


## model调用接口

### api

- api.py
- 拥有所有model的接口

### 线性回归

- linear_regression/linear_regression.py
- 直接显示结果

### 图像合成

- compose/compose.py
- 直接显示结果


### 车牌识别

- lic_detect/lic_detect.py
- 直接显示结果


### 风格迁移

- style_transfer/style_transfer.py
- 结果保存在output目录


### yolo_5

- yolo_5/yolo_5.py

- 结果保存在output目录


### yolo_x

- yolo_x/tools/yolo_x.py
- 可直接运行 demo.sh
- 直接显示结果

## 系统结构原始图

![交互模型](https://user-images.githubusercontent.com/56027589/155711621-9426b534-ae68-4fb4-b740-144cdedc914a.png)

## 系统结构图

![模型2 0](https://user-images.githubusercontent.com/56027589/163784283-dfe88b36-7190-4420-874c-b84f02b7e778.png)
