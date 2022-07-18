from settings import smp_prop

smp = {"smp": 115, "smp2": 100}

prop_tbl = {"smp": smp}


def prop_tbl_api(send_node, proc_node):
    if proc_node == "smp" and smp_prop != 0:
        return smp_prop

    send_node_tbl = prop_tbl.get(send_node, None)

    if send_node_tbl is None:
        raise Exception("didn't find {} table!".format(send_node))

    prop = send_node_tbl.get(proc_node, -1)

    if prop == -1:
        raise Exception("{} table didn't find {} item!".format(send_node, proc_node))

    return prop
