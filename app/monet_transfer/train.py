import os
import torch
import torch.nn as nn
import numpy as np
import cv2
import matplotlib.pyplot as plt

from torchvision.utils import make_grid

from app import GeneratorResNet, Discriminator

import argparse

from torch.utils.data import Dataset, DataLoader
from PIL import Image
import torchvision.transforms as transforms



def make_parser():
    parser = argparse.ArgumentParser("monet train")

    parser.add_argument("-b", "--batch-size", type=int, default=5, help="batch size")

    parser.add_argument("-e", "--epoch", type=int, default=100, help="epoch")
    parser.add_argument(
        "-d", "--devices", default=None, type=int, help="device for training"
    )

    parser.add_argument("-s", "--save_path", default="./weights", type=str, help="outputs save file")

    parser.add_argument("-dp", "--data_path", default="./datasets/train", type=str, help="input file")

    return parser

args = make_parser().parse_args()

# 定义数据
n_epochs = 100
batch_size = 1
sample_interval = 20

cuda = True if torch.cuda.is_available() else False
print(cuda)

# 设置Dataset

class ImageDataset(Dataset):
    # 初始化
    def __init__(self, data_dir, mode='train', transforms=None):
        # 文件夹名字
        A_dir = os.path.join(data_dir, 'photo')
        B_dir = os.path.join(data_dir, 'monet')

        # 整合文件名字 前250为训练数据集，后50为测试数据集
        # files_A = [os.path.join(A_dir, name) for name in sorted(os.listdir(A_dir))]
        # files_B = [os.path.join(A_dir, name) for name in sorted(os.listdir(B_dir))]

        # if mode == 'train':
        # self.files_A = files_A[:250]
        # self.files_B = files_B[:250]
        # elif mode == 'test':
        # self.files_A = files_A[250:300]
        # self.files_B = files_B[250:300]

        if mode == 'train':
            self.files_A = [os.path.join(A_dir, name) for name in sorted(os.listdir(A_dir))[50:1000]]
            self.files_B = [os.path.join(B_dir, name) for name in sorted(os.listdir(B_dir))[50:1000]]
        elif mode == 'test':
            self.files_A = [os.path.join(A_dir, name) for name in sorted(os.listdir(A_dir))[:50]]
            self.files_B = [os.path.join(B_dir, name) for name in sorted(os.listdir(B_dir))[:50]]

        # print(self.files_A[:3])
        self.transforms = transforms

    def __len__(self):
        return len(self.files_A)

    def __getitem__(self, index):
        # 拿到对应的路径
        files_A = self.files_A[index]
        files_B = self.files_B[index]

        # 打开
        img_A = Image.open(files_A)
        img_B = Image.open(files_B)

        # 预处理
        if self.transforms is not None:
            img_A = self.transforms(img_A)
            img_B = self.transforms(img_B)

        return img_A, img_B



# 导入数据
data_dir = args.data_path

# 设置数据预处理方式
transforms_ = transforms.Compose([
    #transforms.Resize(int(256*1.12), Image.BICUBIC),
    #transforms.RandomCrop(256, 256),
    #transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])


# 设置DataLoader
trainloader = DataLoader(
    ImageDataset(data_dir, mode='train', transforms=transforms_),
    batch_size=batch_size,
    shuffle = True,
    num_workers= 3)

testloader = DataLoader(
    ImageDataset(data_dir, mode='test', transforms=transforms_),
    batch_size=batch_size,
    shuffle = False,
    num_workers= 3)


# 定义损失函数
criterion_GAN = nn.MSELoss()        # 生成器与判别器的损失函数
criterion_cycle = nn.L1Loss()       # 由假A(B)生成的假B(A)与真B(A)的损失函数
criterion_identity = nn.L1Loss()    # 由真A(B)生成的假A(B)与真A(B)的损失函数


# 定义生成器与判别器
G_AB = GeneratorResNet(3, num_residual_blocks=9)
D_B = Discriminator(3)

G_BA = GeneratorResNet(3, num_residual_blocks=9)
D_A = Discriminator(3)


# 放入gpu
print(f'cuda: {cuda}')
if cuda:
    G_AB = G_AB.cuda()
    D_B = D_B.cuda()
    G_BA = G_BA.cuda()
    D_A = D_A.cuda()

    criterion_GAN = criterion_GAN.cuda()
    criterion_cycle = criterion_cycle.cuda()
    criterion_identity = criterion_identity.cuda()

# 定义优化器
import itertools
lr = 0.0002
b1 = 0.5
b2 =0.999

optimizer_G = torch.optim.Adam(
    itertools.chain(G_AB.parameters(), G_BA.parameters()),
    lr=lr,
    betas=(b1, b2)
)

optimizer_D_A = torch.optim.Adam(
    D_A.parameters(),
    lr=lr,
    betas=(b1, b2)
)

optimizer_D_B = torch.optim.Adam(
    D_B.parameters(),
    lr=lr,
    betas=(b1, b2)
)


# 学习率设置
lambda_func = lambda epoch: 1 - max(0, epoch-sample_interval)/(n_epochs-sample_interval)

lr_scheduler_G = torch.optim.lr_scheduler.LambdaLR(optimizer_G, lr_lambda=lambda_func)
lr_scheduler_D_A = torch.optim.lr_scheduler.LambdaLR(optimizer_D_A, lr_lambda=lambda_func)
lr_scheduler_D_B = torch.optim.lr_scheduler.LambdaLR(optimizer_D_B, lr_lambda=lambda_func)


# 展示图片模块


Tensor = torch.cuda.FloatTensor if cuda else torch.FloatTensor

'''def display_images(real_A, real_B, figside=1.5):
    # 验证两图片格式是否相同
    assert real_A.size() == real_B.size(), 'The image size for two domains must be the same'

    G_AB.eval()
    G_BA.eval()

    real_A = real_A.type(Tensor)
    fake_B = G_AB(real_A).detach()
    real_B = real_B.type(Tensor)
    fake_A = G_BA(real_B).detach()

    nrows = real_A.size(0)

    real_A = make_grid(real_A, nrow=nrows, normalize=True)
    fake_B = make_grid(fake_B, nrow=nrows, normalize=True)
    real_B = make_grid(real_B, nrow=nrows, normalize=True)
    fake_A = make_grid(fake_A, nrow=nrows, normalize=True)

    image_grid = torch.cat((real_A, fake_B, real_B, fake_A), 1).cpu().permute(1, 2, 0)

    plt.figure(figsize=(figside*nrows, figside*4))
    plt.imshow(image_grid)
    plt.axis('off')
    plt.show()'''

'''# 展示
real_A, real_B = next(iter(testloader))
display_images(real_A, real_B)'''


# 开始训练
print('Start train')

# 保存模型路径
pth_dir = './weights'
if not os.path.exists(pth_dir):
    os.makedirs(pth_dir)


for epoch in range(n_epochs):
    for i, (real_A, real_B) in enumerate(trainloader):
        # 不是很懂，不是已经是tensor了么？？
        real_A, real_B = real_A.type(Tensor), real_B.type(Tensor)

        # 建立标签(16*16的全'1'与全'0')
        out_shape = [real_A.size(0), 1, real_A.size(2)//D_A.scale_factor, real_A.size(3)//D_A.scale_factor]
        valid = torch.ones(out_shape).type(Tensor)
        fake = torch.zeros(out_shape).type(Tensor)

        # 准备工作

        # display_images中把生成器关掉了(.eval), 所以先打开
        G_AB.train()
        G_BA.train()

        # 梯度清零
        optimizer_G.zero_grad()

        # 过图
        fake_B = G_AB(real_A)
        fake_A = G_BA(real_B)
        recov_A = G_BA(fake_B)
        recov_B = G_AB(fake_A)
        sim_A = G_BA(real_A)
        sim_B = G_AB(real_B)

        # 生成器损失值
        loss_g_AB = criterion_GAN(D_B(fake_B), valid)
        loss_g_BA = criterion_GAN(D_A(fake_A), valid)
        loss_g = (loss_g_AB + loss_g_BA) / 2

        # cycleloss
        loss_cycle_A = criterion_cycle(recov_A, real_A)
        loss_cycle_B = criterion_cycle(recov_B, real_B)
        loss_cycle = (loss_cycle_A + loss_cycle_B) / 2

        # identityloss
        loss_identity_A = criterion_identity(sim_A, real_A)
        loss_identity_B = criterion_identity(sim_B, real_B)
        loss_identity = (loss_identity_A + loss_identity_B) / 2

        # 总损失值
        loss_G = 5.0*loss_identity + loss_g + 10.0*loss_cycle
        loss_G.backward()
        optimizer_G.step()

        #判别器A
        optimizer_D_A.zero_grad()

        loss_real_A = criterion_GAN(D_A(real_A), valid)
        loss_fake_A = criterion_GAN(D_A(fake_A.detach()), fake)
        loss_D_A = (loss_real_A + loss_fake_A) / 2

        loss_D_A.backward()
        optimizer_D_A.step()

        # 判别器B
        optimizer_D_B.zero_grad()

        loss_real_B = criterion_GAN(D_B(real_B), valid)
        loss_fake_B = criterion_GAN(D_B(fake_B.detach()), fake)
        loss_D_B = (loss_real_B + loss_fake_B) / 2

        loss_D_B.backward()
        optimizer_D_B.step()

    # 每过一个epoch更新一次学习率
    lr_scheduler_G.step()
    lr_scheduler_D_A.step()
    lr_scheduler_D_B.step()

    # test
    
    test_A, test_B = next(iter(testloader))

    loss_D = (loss_D_A + loss_D_B) / 2

    print(f'[Epoch {epoch+1}/{n_epochs}]')
    print(f'[G loss : {loss_G.item()} | GAN : {loss_g.item()} | cycle : {loss_cycle.item()} | identity : {loss_identity.item()}]')
    print(f'[D loss : {loss_D.item()} | D_A : {loss_D_A.item()} | D_B : {loss_D_B.item()}]')

    if epoch % 10 == 0:
        torch.save(G_BA.state_dict(), './weights/G_BA_' + str(epoch+1) + '.pth')
        torch.save(G_AB.state_dict(), './weights/G_AB_' + str(epoch+1) + '.pth')


'''# 生成艺术照
photo_dir = os.path.join(data_dir, 'photo_jpg')
files = [os.path.join(photo_dir, name) for name in os.listdir(photo_dir)]
len(files)

save_dir = '../images'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

generate_transforms = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

to_image = transforms.ToPILImage()

G_AB.eval()
for i in range(0, len(files), batch_size):
    # read images
    imgs = []
    for j in range(i, min(len(files), i + batch_size)):
        img = Image.open(files[j])
        img = generate_transforms(img)
        imgs.append(img)
    imgs = torch.stack(imgs, 0).type(Tensor)

    # generate
    fake_imgs = G_AB(imgs).detach().cpu()

    # save
    for j in range(fake_imgs.size(0)):
        img = fake_imgs[j].squeeze().permute(1, 2, 0)
        img_arr = img.numpy()
        img_arr = (img_arr - np.min(img_arr)) * 255 / (np.max(img_arr) - np.min(img_arr))
        img_arr = img_arr.astype(np.uint8)

        img = to_image(img_arr)
        _, name = os.path.split(files[i + j])
        img.save(os.path.join(save_dir, name))'''


