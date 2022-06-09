# This is wgk's *十万个为什么*
[toc]

## 数据结构问题

### node.py

* task_queue 和 frame_queue 有什么区别？一个是任务队列，一个是帧任务队列:
    * 是否可以这样认为：帧任务队列是处于当前的思路选择，主要是进行图片的处理，所以帧任务队列相当于只发送图像处理的任务队列


## 函数问题

### task_service.py

* TaskServer.update_tasks()函数是用来更新节点的任务队列，功能有添加任务和删除任务两种方式，但是为什么：
    * 节点的任务处理时间 *node.task_start_time* 是从这里开始赋值的？这明显是一个对节点的全局任务处理时间计数，为什么会在这里进行赋值？难道我每往节点运行队列中添加一次任务，这个时间就会更新一次？那么这个值有什么意义。

## module.node_discovery.Const.py

* 庆庆为了省事直接将我的代码照搬过来，导致这里存在一个class Node，与node.py中的class Node同名, 这里接下来注意改一下