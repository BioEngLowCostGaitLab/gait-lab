import torch
import torch.nn.functional as F
import torch.nn as nn
from torchvision import transforms
from torchvision.utils import save_image
from torch.utils import data
from torch.autograd import Variable
from matplotlib import pyplot as plt
import numpy as np
import os
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
		self.batchnorm2 = nn.BatchNorm2d(2 * fSize)
		self.conv3 = nn.Conv2d(fSize * 2, fSize * 4, 4, stride=2, padding=1, bias=False)
        # 4*fSize x 4 x 4
		self.batchnorm3 = nn.BatchNorm2d(4 * fSize)
		self.conv4 = nn.Conv2d(fSize * 4, fSize * 8, 4, stride=2, padding=1, bias=False)
        # 8*fSize x 2 x 2
		self.batchnorm4 = nn.BatchNorm2d(8 * fSize)

		self.conv5 = nn.Conv2d(fSize * 8, 1, 4, stride=2, padding=1, bias=False)

		self.fc1 = nn.Linear(2048, 1000)
		self.fc2 = nn.Linear(1000, 1)

		self.lRelu = nn.LeakyReLU(0.2, inplace=True)

	def forward(self, x):
		# forward pass of network
		x = self.lRelu(self.conv1(x))
		x = self.lRelu(self.batchnorm2(self.conv2(x)))
		x = self.lRelu(self.batchnorm3(self.conv3(x)))
		x = self.lRelu(self.batchnorm4(self.conv4(x)))
		x = F.sigmoid(self.conv5(x))

		return x

	def save_params(self, exDir):
		print('saving params...')
		torch.save(self.state_dict(), join(exDir, 'edp_params'))

	def load_params(self, exDir):
		print('loading params...')
		self.load_state_dict(torch.load(join(exDir, 'edp_params')))

transform = transforms.ToTensor()

trainset = Markers(transform=transform)
testset = Markers(train=False, transform=transform)

trainloader = data.DataLoader(trainset, batch_size=2,
                                          shuffle=True,
                                          num_workers=2)
testloader = data.DataLoader(testset, batch_size=2,
                                          shuffle=False,
                                          num_workers=2)





net = Net(fSize=64)
optimiser = optim.Adam(net.parameters(), lr=1e-3)


for epoch in range(10):

	for i, data in enumerate(trainloader):
		x, labels = data
		labels = torch.FloatTensor(labels)
		labels.unsqueeze_(-1)
		x, labels = Variable(x), Variable(labels)
		preds = net.forward(x)

		loss = F.binary_cross_entropy(preds, labels)

		optimiser.zero_grad()
		loss.backward()
		optimiser.step()

	test_correct = 0
	for i, data in enumerate(testloader):
		x, labels = data
		x = Variable(x)
		preds = net.forward(x)
		for k in range(len(preds)):
			if preds[k].data.numpy() - labels[k] < 0.5:
				test_correct += 1

	test_accurary = test_correct / testset.__len__()

	print('%d accuracy %.2f' % (epoch, test_accurary))

net.save_params(os.getcwd())
