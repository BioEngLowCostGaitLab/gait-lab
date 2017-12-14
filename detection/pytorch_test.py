import torch
import torch.nn.functional as F
import torch.nn as nn
from torchvision import transforms
from torchvision.utils import save_image
from torch.utils import data
from torch.autograd import Variable
from matplotlib import pyplot as plt
import numpy as np
from os.path import join, exists
from torch import optim
import argparse
from time import time
from dataload import Markers


class Net(nn.Module):

	def __init__(self, fSize):
		super(Net, self).__init__()
		#define layers here
        self.fSize = fSize
		# 3 x 32 x 32
		self.conv1 = nn.Conv2d(3, fSize, 4, stride=2, padding=1, bias=False)
        # fSize x 16 x 16
		self.conv2 = nn.Conv2d(fSize, fSize * 2, 4, stride=2, padding=1, bias=False)
        # 2*fSize x 8 x 8
		self.encbatchnorm2 = nn.BatchNorm2d(2 * fSize)
		self.conv3 = nn.Conv2d(fSize * 2, fSize * 4, self.kernelSize, stride=2, padding=1, bias=False)
        # 4*fSize x 4 x 4
		self.encbatchnorm3 = nn.BatchNorm2d(4 * fSize)
		self.conv4 = nn.Conv2d(fSize * 4, fSize * 8, self.kernelSize, stride=2, padding=1, bias=False)
        # 8*fSize x 2 x 2
		self.encbatchnorm4 = nn.BatchNorm2d(8 * fSize)

        self.fc1 = nn.Linear(2048, 1000)
        self.fc2 = nn.Linear(1000, 1)

        self.lRelu = nn.LeakyReLU(0.2, inplace=True)

	def forward(self, x):
		# forward pass of network
		x = self.lRelu(self.enc1(x))
		x = self.lRelu(self.encbatchnorm2(self.enc2(x)))
		x = self.lRelu(self.encbatchnorm3(self.enc3(x)))
		x = self.lRelu(self.encbatchnorm4(self.enc4(x)))
		x = x.view(x.size(0), -1)
        x = self.lRelu(self.fc1(x))
        x = F.sigmoid(self.fc2(x))

		return x

transform = tranforms.ToTensor()

trainset = Markers(transform=transform)
testset = Markers(train=False, transform=transform)

trainloader = data.Dataloader(trainset, batch_size=2,
                                          shuffle=True,
                                          num_workers=2)
testloader = data.Dataloader(testset, batch_size=2,
                                          shuffle=False,
                                          num_workers=2)





net = Net(fSize=64)
criterion = nn.CrossEntropyLoss()
optimiser = optim.Adam(net.parameters(), lr=1e-3)


for epoch in range(40):

	for i, data in enumerate(trainloader):
