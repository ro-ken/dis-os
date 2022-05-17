import os
import time


def write_file(path, data, type='wb'):
    path_dir = os.path.split(path)[0]
    if not os.path.exists(path_dir):
        os.makedirs(path_dir)
    f = open(path, type)
    f.write(data)
    f.close()


def mytime(int_len=100000, point_len=2):
    return round(time.time() % int_len, point_len)


def write_task_seq(path, seq, task_list, info, type='a+', new_line=False):
    data = "the {} times, {} , {} , time={}\n".format(seq, task_list, info, mytime())
    if new_line:
        data = '\n' + data
    write_file(path, data, type)


def write_time_start(path, title, type='a+'):
    data = title + " start time :" + str(mytime()) + '\n'
    print()
    write_file(path, data, type)


def write_time_end(path, title):
    data = title + " end   time :" +str(mytime()) + '\n'
    write_file(path, data, 'a+')