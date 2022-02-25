import os

import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

def run():
    adv_data = pd.read_csv(os.path.split(os.path.realpath(__file__))[0] + "/data.csv")
    new_adv_data = adv_data.iloc[:,0:3]

    sns.pairplot(new_adv_data, x_vars=['size', 'number'], y_vars='price', height=7, aspect=0.8, kind='reg')
    plt.savefig("pairplot.jpg")
    #plt.show()

    X_train, X_test, Y_train, Y_test = train_test_split(new_adv_data.iloc[:,:2], new_adv_data.price, train_size=.80)
    model = LinearRegression()

    model.fit(X_train, Y_train)

    a = model.intercept_  # 截距

    b = model.coef_  # 回归系数

    # print("最佳拟合线:截距", a, ",回归系数：", b)
    # y=2.668+0.0448∗TV+0.187∗Radio-0.00242∗Newspaper
    y = a+b[0]*2000+b[1]*1

    score = model.score(X_test, Y_test)

    print(score)

    # 对线性回归进行预测

    Y_pred = model.predict(X_test)

    print(Y_pred)

    plt.plot(range(len(Y_pred)), Y_pred, 'b', label="predict")
    plt.figure()
    plt.plot(range(len(Y_pred)), Y_pred, 'b', label="predict")
    plt.plot(range(len(Y_pred)), Y_test, 'r', label="test")
    plt.legend(loc="upper right")  # 显示图中的标签
    plt.xlabel("the number of sales")
    plt.ylabel('value of sales')
    # plt.savefig("ROC.jpg")
    try:
        while(True):
            plt.show()
    except(KeyboardInterrupt,SystemExit):
        pass
if __name__ == '__main__':
    run()



