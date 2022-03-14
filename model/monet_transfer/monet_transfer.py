import os
import torch
import torch.nn as nn
import numpy as np
import cv2
import matplotlib.pyplot as plt

from torchvision.utils import make_grid

from torch.utils.data import Dataset, DataLoader
from PIL import Image
import torchvision.transforms as transforms

import argparse

from .model import GeneratorResNet

ROOT = os.path.split(os.path.realpath(__file__))[0] + '/'

def start():

    batch_size = 1
    cuda = True if torch.cuda.is_available() else False
    # print(cuda)

    def make_parser():
        parser = argparse.ArgumentParser("monet detect")

        parser.add_argument(
            "-d", "--devices", default=None, type=int, help="device for training"
        )

        parser.add_argument("-s", "--save_path", default=ROOT + "outputs", type=str, help="outputs save file")

        parser.add_argument("-c", "--ckpt", default=ROOT + "weights/G_AB.pth", type=str, help="checkpoint file")

        parser.add_argument("-dp", "--data_path", default=ROOT + "datasets/input", type=str, help="input file")

        return parser


    args = make_parser().parse_args()

    # 导入数据
    data_dir = args.data_path


    # 定义生成器
    G_AB = GeneratorResNet(3, num_residual_blocks=9)
    # 放入gpu

    if cuda:
        print(f'cuda: {cuda}')
        G_AB = G_AB.cuda()
        G_AB.load_state_dict(torch.load(args.ckpt))
    else:
        G_AB.load_state_dict(torch.load(args.ckpt, map_location=torch.device('cpu')))
    #G_BA = GeneratorResNet(3, num_residual_blocks=9)


    Tensor = torch.cuda.FloatTensor if cuda else torch.FloatTensor

    # 生成艺术照
    photo_dir = data_dir
    files = [os.path.join(photo_dir, name) for name in os.listdir(photo_dir)]
    len(files)

    save_dir = args.save_path
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
            img.save(os.path.join(save_dir, name))
        # print("ok")

if __name__ == '__main__':
    start()