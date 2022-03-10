import torch
import torch.nn as nn

# 定义生成器
# 定义残差网络
class ResidualBlock(nn.Module):
    def __init__(self, in_channels):
        super(ResidualBlock, self).__init__()
        self.block = nn.Sequential(
            nn.ReflectionPad2d(1),   # padding, keep the image size constant after next conv2d
            nn.Conv2d(in_channels, in_channels, 3),
            nn.InstanceNorm2d(in_channels),
            nn.ReLU(inplace=True),
            nn.ReflectionPad2d(1),
            nn.Conv2d(in_channels, in_channels, 3),
            nn.InstanceNorm2d(in_channels)
        )

    def forward(self, x):
        return x + self.block(x)


# 生成器
class GeneratorResNet(nn.Module):
    def __init__(self, in_channels, num_residual_blocks=9):
        super(GeneratorResNet, self).__init__()

        # conv->down->ResidualBlock->up->out

        #conv   3*256*256 -> 64*256*256
        out_channels = 64
        self.conv = nn.Sequential(
            nn.ReflectionPad2d(in_channels),
            nn.Conv2d(in_channels, out_channels, 2*in_channels+1),
            nn.InstanceNorm2d(out_channels),
            nn.ReLU(inplace=True)
        )

        # down  64*256*256 -> 128*128*128 -> 256*64*64
        channels = out_channels     # 64
        self.down = []
        for _ in range(2):
            out_channels = channels * 2     # 128
            self.down += [
                nn.Conv2d(channels, out_channels, 3, stride=2, padding=1),
                nn.InstanceNorm2d(out_channels),
                nn.ReLU(inplace=True),
            ]
            channels = out_channels
        self.down = nn.Sequential(*self.down)

        # ResidualBlock * 9     256*64*64
        self.trans = [ResidualBlock(channels) for _ in range(num_residual_blocks)]
        self.trans = nn.Sequential(*self.trans)

        #up     256*64*64 -> 128*128*128 -> 64*256*256
        self.up = []
        for _ in range(2):
            out_channels = channels // 2     # 128
            self.up += [
                nn.Upsample(scale_factor=2),
                nn.Conv2d(channels, out_channels, 3, stride=1, padding=1),
                nn.InstanceNorm2d(out_channels),
                nn.ReLU(inplace=True),
            ]
            channels = out_channels
        self.up = nn.Sequential(*self.up)

        # out   64*256*256 -> 3*256*256
        self.out = nn.Sequential(
            nn.ReflectionPad2d(in_channels),
            nn.Conv2d(channels, in_channels, 2*in_channels+1),
            nn.Tanh()
        )

    def forward(self, x):
        x = self.conv(x)
        x = self.down(x)
        x = self.trans(x)
        x = self.up(x)
        x = self.out(x)
        return x


class Discriminator(nn.Module):

    def block(self, in_channels, out_channels, normalize=True):
        layers = [nn.Conv2d(in_channels, out_channels, 4, stride=2, padding=1)]
        if normalize:
            layers.append(nn.InstanceNorm2d(out_channels))
        layers.append(nn.LeakyReLU(0.2, inplace=True))

        return layers

    def __init__(self, in_channels):
        super(Discriminator, self).__init__()

        self.model = nn.Sequential(

            # 为什么不标准化？
            *self.block(in_channels, 64, normalize=False),  # 3*256*256 -> 64*128*128
            *self.block(64, 128),       # 64*128*128 -> 128*64*64
            *self.block(128, 256),      # 128*64*64 -> 256*32*32
            *self.block(256, 512),      # 256*32*32 -> 512*16*16
            # pathGAN
            # 为什么要填充？
            nn.ZeroPad2d((1, 0, 1, 0)), #左边+上边填充0   512*16*16 -> 512*17*17
            nn.Conv2d(512, 1, 4, padding=1)     # 512*17*17 -> 1*16*16

        )

        self.scale_factor = 16

    def forward(self, x):
        x = self.model(x)
        return x