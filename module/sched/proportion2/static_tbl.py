
need_node_num = 3


prop_tbl = {"local" : 10,"smp": 3.5,"rpb": 3.4,"rpc": 2.9 ,"rpd":1,"ywd":3.3,"hwj":8}



def prop_tbl_api(send_node, proc_node):
    # if proc_node == "smp" and smp_prop != 0:
    #     return smp_prop

    # send_node_tbl = prop_tbl.get(send_node, None)
    send_node_tbl = prop_tbl     # 不考虑传输时延差异

    # todo
    # if send_node_tbl is None:
    #     raise Exception("didn't find {} table!".format(send_node))

    prop = send_node_tbl.get(proc_node, -1)

    if prop == -1:
        raise Exception("{} table didn't find {} item!".format(send_node, proc_node))

    return prop
