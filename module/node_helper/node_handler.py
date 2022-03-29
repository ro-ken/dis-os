import time

import server_node
import client_node
import settings


class NodeHandler:

    def __init__(self, master):
        self.master = master

    # 对每个node建立一个client与之连接
    def create_clients(self):
        for node in self.master.node_list:
            ip, port = node[0], node[1]
            client_t = client_node.ClientThread(ip, port, self.master)
            client_t.start()
            self.master.client_list.append(client_t)
            time.sleep(1)


    # 通过调度模块方法获取节点地址, 开始进行测试
    def do_work(self):
        # 本机测试
        if settings.env == "dev":
            for client in self.master.client_list:
                # 给每个client添加任务
                client.handler.add_tasks(range(7))
        else:
            # 联机测试
            # task_list = utils.get_random(15)
            task_list = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6]
            print(task_list)
            res = self.master.scheduler.divide_tasks(task_list, self.master.node_resources)
            print(res)
            for i in range(3):
                self.master.client_list[i].add_tasks(res[i])
            while True:
                for client in self.master.client_list:
                    if client.disconnect:
                        res_task = client.task_queue.copy()
                        self.master.client_list.remove(client)
                        self.master.client_list[0].add_tasks(res_task)
