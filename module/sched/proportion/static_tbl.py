smp = {"smp": 1, "smp2": 2, "smp3": 3}

prop_tbl = {"smp": smp}


def prop_tbl_api(send_node, proc_node):
    send_node_tbl = prop_tbl.get(send_node, None)

    if send_node_tbl is None:
        raise Exception("didn't find {} table!".format(send_node))

    prop = send_node_tbl.get(proc_node, -1)

    if prop == -1:
        raise Exception("{} table didn't find {} item!".format(send_node, proc_node))

    return prop
