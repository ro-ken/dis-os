import random

taskarray = []


def product():
    taskarray = []
    for i in range(9):
        number = random.randint(0, 8)
        taskarray.append(number)
    print(taskarray)
    s = test(taskarray)
    if s == 0:
        product()


def test(taskarray):
    repeat = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(9):
        repeat[taskarray[i]] = repeat[taskarray[i]] + 1
    for i in range(len(repeat)):
        print(repeat[i])
        if repeat[i] > 3:
            return 0
    return 1


if __name__ == '__main__':
    product()
