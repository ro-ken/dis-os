from model import api
from tools import utils

path = utils.ROOT + 'output/resource.txt'

utils.save_resource(path,type='w')
utils.write_time_start(path,'task0')
api.run([0])
utils.write_time_start(path,'task1')
utils.save_resource(path)
api.run([1])
utils.write_time_start(path,'task2')
utils.save_resource(path)
api.run([2])
utils.save_resource(path)
utils.write_time_start(path,'task3')
api.run([3])
utils.save_resource(path)
utils.write_time_start(path,'task4')
api.run([4])
utils.save_resource(path)
utils.write_time_start(path,'task5')
api.run([5])
utils.save_resource(path)
utils.write_time_start(path,'task6','w')
# api.run([6])
# utils.save_resource(path)
# utils.write_time_start(path,'task0','w')