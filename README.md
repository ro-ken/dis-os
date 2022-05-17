# dis-os


## 项目地址

**github**：https://github.com/ro-ken/dis-os

**gitee**：https://gitee.com/ro_ken/dis-os   （可能会存在滞后）

## 项目运行

**1、安装库**

> 依赖库文件在tools目录下的requirements.txt文件中，
>
> **安装命令**：
>
> ```
> pip install -r requirements.txt -i https://pypi.douban.com/simple
> ```
>
> 有些比较难装的库可单独安装，不然因为一个库，所有库都要重新装一遍

**2、配置**

> 在根目录有个settings.py，是程序的主配置文件
>
> 主要是对程序运行的任务进行控制
>
> 如果不能运行TensorFlow，arch不要选win

**3、启动**

> 如果库都装安装成功，运行node应该是可以正常启动的
>
> ```
> python node.py
> ```
>
> 在本机也可以启动多个终端运行程序
>
> 没有任务的话，不同节点之间能互相发生心跳


## 目录结构

```
  .
  ├── dataset           # 数据集
  ├── exper             # 做的一些实验测试
  ├── app               # 任务模型
  │   ├── app_api.py           # 供上层调用的任务API
  │   └── app_api_local.py     # 本地的任务测试文件
  │
  ├── module           # 一些独立的模块
  │   ├── group             # 小组成员的个人的文件（无关）
  │   ├── proto             # grpc的定义的接口
  │   ├── node_discovery    # udp节点发现模块
  │   ├── node_helper
  │   │   ├── node_handler.py    # 节点的辅助类，一些业务函数封装在里面
  │   │   └── node_struct.py     # 节点的一些数据结构
  │   │
  │   ├── sched        # 节点的任务调度器
  │   │   ├── sched.py        # 调度器接口，具体的调度类要继承这个接口类
  │   │   └── sched_api.py    # 供上层函数选择用哪个接口  
  │   │
  │   └── task_helper         # client、server的辅助类
  │       ├── client_handler.py    # client_handler的辅助类，一些业务函数
  │       ├── task_handler.py      # grpc接口在client端的函数
  │       ├── task_service.py      # grpc接口在server端的实现
  │       └── task_testy.py        # 做任务测试
  │
  ├── tools
  │   ├── requirements.txt    # 需要的依赖
  │   ├── node_settings       # 主节点的一些配置
  │   ├── utils.py            # 通用的方法
  │   ├── io_utils.py         # 文件IO通用的方法
  │   └── random_num.py       # 生成随机数的文件
  │
  ├── settings.py             # 主配置文件
  ├── node.py                 # 主启动类
  ├── client_node.py          # client线程
  └── server_node.py          # server线程

```

## 图

### 系统结构原始图

![交互模型](https://user-images.githubusercontent.com/56027589/155711621-9426b534-ae68-4fb4-b740-144cdedc914a.png)

### 系统结构图

![模型3 0](https://user-images.githubusercontent.com/56027589/168619782-033a2419-f18e-4455-ad6e-1295ecfe8623.png)

### 流程图

![流程图](https://user-images.githubusercontent.com/56027589/165533730-cf12b8a3-fc5d-47f8-b36f-c34efc1d32d5.png)

### 数据结构图

![数据结构图](https://user-images.githubusercontent.com/56027589/168620091-6ca23866-02dc-4352-935f-6a82057707b1.jpg)

