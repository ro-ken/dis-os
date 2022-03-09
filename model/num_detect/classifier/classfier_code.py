#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@ModuleName: classfier_code
@Function: 完成一个数字识别功能的卷积神经网络的训练
@Author: PengKai
@Time: 2020/4/30 22:43
"""

import os
import torch
from torchvision import transforms
from torchvision import datasets
from torch.utils.data import DataLoader
import torch.nn.functional as F
import torch.optim as optim

ROOT = os.path.split(os.path.realpath(__file__))[0] + '/'


batch_size = 64
transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
# 下载训练数据集
train_dataset = datasets.MNIST(root=ROOT + 'dataset',
                            train=True, download=True, transform=transform)
train_loader = DataLoader(train_dataset, shuffle=True, batch_size=batch_size)
# 下载测试数据集
test_dataset = datasets.MNIST(root='dataset',
                            train=False, download=True, transform=transform)
test_loader = DataLoader(test_dataset,shuffle=False,batch_size=batch_size)


class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = torch.nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = torch.nn.Conv2d(10, 20, kernel_size=5)
        self.pooling = torch.nn.MaxPool2d(2)
        self.fc = torch.nn.Linear(320, 10)

    def forward(self,x):
        batch_size = x.size(0)
        x = F.relu(self.pooling(self.conv1(x)))
        x = F.relu(self.pooling(self.conv2(x)))
        x = x.view(batch_size, -1)
        x = self.fc(x)
        return x


model = Net()
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model.to(device)
criterion = torch.nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.5)


# 训练数据集
def train(epoch):
    running_loss = 0.0
    for batch_idx, data in enumerate(train_loader, 0):
        inputs, target = data
        inputs, target = inputs.to(device), target.to(device)
        optimizer.zero_grad()

        # 计算损失函数
        outputs = model(inputs)
        loss = criterion(outputs,target)
        loss.backward()
        # 更新
        optimizer.step()
        # 计算总的损失值
        running_loss += loss.item()
        if batch_idx % 300 == 299:
            print('[%d,%5d]loss:%.3f'%(epoch + 1, batch_idx + 1, running_loss / 2000))
            running_loss = 0.0


# 测试集
def test():
    correct = 0
    total = 0
    with torch.no_grad():
        for data in test_loader:
            images, target = data
            images = images.to(device)
            target = target.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, dim=1)
            total += target.size(0)
            correct += (predicted == target).sum().item()
        print('正确率为:%.2f %%' % (100 * correct / total))


# 保存模型
def save_model():
    ckpt_dir =ROOT + '/model'
    save_path = os.path.join(ckpt_dir, 'CNN_MNIST_model.pth.tar')
    torch.save({'state_dict': model.state_dict()}, save_path)


if __name__ == '__main__':
    for epoch in range(10):
        train(epoch)
        test()
        if epoch == 9:
            save_model()
