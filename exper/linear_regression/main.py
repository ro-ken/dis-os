import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model

row_len = 12
size = 11
def run():
    a=[]
    b=[]
    num=0
    for i in range(11):
        multilist = [[0 for col in range(row_len)] for row in range(size)]
        #print(type(multilist))
        i=str(i*10)
        f = open("data/smp_old/local_task_time_cpu_"+i+".txt",encoding="utf-8")
        for line in f.readlines():
            trash, time = line.split(':')
            j,k = time.split('\n')
            a.append(trash)
            if j != '':
                b.append(j)
    # print(b)
    for i in range(11):
        for j in range(row_len):
            multilist[i][j]=b[num]
            num+=1
            #print(a+"yh"+b)
        #print(f.readlines())
        f.close()
    # for i in range(11):
    #     for j in range(row_len):
    #         print(multilist[i][j])
    #     print('\n')


    for j in range(6):
        num = []
        num1 = []
        for i in range(10):

            tmp = float(multilist[i][j*2+1])-float(multilist[i][j*2])
            # n = 3
            # temp1 = float(multilist[i][j*2+1])-float(multilist[i][j*2])
            # temp2 = float(multilist[i][12+j*2+1])-float(multilist[i][12+j*2])
            # temp3 = float(multilist[i][24+j*2+1])-float(multilist[i][24+j*2])
            # tmp = (temp1 + temp2 + temp3 )/3
            # if temp3 <0:
            #     tmp = (temp1 + temp2)/2
            # print("temp1 = {} ,temp2 = {} , temp3 = {}".format(temp1,temp2,temp3))
            num.append(float(tmp))
            num1.append(int(i)*10)
    #plt.figure(figsize=10)
        plt.title('pic')
        plt.xlabel('cpu ratio %')
        plt.ylabel('time/s')
        plt.plot(num1,num)
        x=np.array(num1).reshape(-1,1)
        y=np.array(num)
        linear(x,y)
    plt.show()

def linear(x,y):
    model = linear_model.LinearRegression()
    model.fit(x,y)
    j = np.arange(0,100,1)
    k = model.coef_*j+model.intercept_
    plt.plot(j,k)
    print("a = "+str(model.coef_)+" b="+str(model.intercept_))
if __name__ == '__main__':
    run()



