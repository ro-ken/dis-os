# dis-os

## 目录结构

- dataset：数据集

- model：任务模型

- tools
  
    - /proto/：传输格式
    - settings.py：配置文件
    - requirements.txt:需要的依赖
    - utils.py:通用的方法
    - sched.py:调度策略
    - task_handler:client的任务助手
    - task_service:server的任务助手

- node.py启动项目

- client发送任务

- server处理任务


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

## 系统结构图

![交互模型](https://user-images.githubusercontent.com/56027589/155711621-9426b534-ae68-4fb4-b740-144cdedc914a.png)

