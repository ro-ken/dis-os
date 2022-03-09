# dis-os

## 目录结构

- dataset：数据集

- model：任务模型

- proto：传输格式

- tools
  
    - settings.py：配置文件
    - requirements.txt:需要的依赖
    - utils.py:通用的方法

- node.py启动项目

- client发送任务

- server处理任务


## model调用接口

### ai

- ai.py
- 直接显示结果

### face_ai

- faceai/compose.py
- 直接显示结果


### lic_detect

- detect_rec_img.py
- **在ubuntu里 132行改为：idx = i**
- 直接显示结果


### style_transfer

- train.py
- 结果保存在output目录


### yolo5

- detect.py

- 结果保存在output目录


### yolox

- tools/demo.py
- 可直接运行 demo.sh
- 直接显示结果

## 系统结构图

![交互模型](https://user-images.githubusercontent.com/56027589/155711621-9426b534-ae68-4fb4-b740-144cdedc914a.png)

