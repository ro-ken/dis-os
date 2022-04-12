# DynNode module

* DynNode module负责节点管理, 包括节点动态加入和退出, 节点间控制交流和命令交流(不包括数据交流, 原因见下文)

## Module structure

```python
DynNode modlue
+-- Const.py
    +-- class Node
        +-- NodeJoin
        +-- NodeRemove
        +-- NodeModSource
+-- DynNode.py
+-- DynNodeServer.py
+-- README.md

'''
message format
"message type is a dict"
message = {
    type : message_type,
    data : message_data, // 用来传递一些附加信息
}
allowed message type:
    +- JOIN     - 节点加入集群
    +- REMOVE   - 节点移出集群
因为此处我们只是使用socket作为节点动态管理, 暂时不考虑用作数据传输, 故消息格式比较简单
'''
```
## Const.py

* class Node是节点表类
* class Node公开了三个方法：
    * NodeJoin: 新节点加入集群
    * NodeRemove: 节点移出集群
    * NodeModSource: 修改节点硬件资源特征

* NodeTable是使用class node生成的节点表, 集群中每一个节点都维护一张节点表, 存储集群中其他节点的ip和port, 并所有节点表都维护一个状态.


## 备注

### 不使用socket进行节点间数据传输
* 因为刚刚接触socket, 并不太了解其特性, 不知道其使用TCP在数据传输方面的特性(安全, 速度等), 而且之前实用grpc已经有一套良好的数据传输框架了