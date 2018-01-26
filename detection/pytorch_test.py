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
		# 3 x 24 x 24
		self.conv1 = nn.Conv2d(3, fSize, 3, stride=2, padding=1)
        # fSize x 16 x 16
		self.conv2 = nn.Conv2d(fSize, fSize * 2, 3, stride=2, padding=0)
        # 2*fSize x 8 x 8
		self.conv3 = nn.Conv2d(fSize * 2, fSize * 4, 3, stride=2, padding=1)
        # 4*fSize x 4 x 4
		self.conv4 = nn.Conv2d(fSize * 4, 1, 3, stride=1, padding=0)
        # 8*fSize x 2 x 2

	def forward(self, x):
		# forward pass of network
		x = F.relu(self.conv1(x))
		x = F.relu(self.conv2(x))
		x = F.relu(self.conv3(x))
		x = F.sigmoid(self.conv4(x))

		return x

	def save_params(self, exDir):
		print('saving params...')
		torch.save(self.state_dict(), join(exDir, 'edp_params1'))

	def load_params(self, exDir):
		print('loading params...')
		self.load_state_dict(torch.load(join(exDir, 'edp_params1')))

transform = transforms.ToTensor()

trainset = Markers(transform=transform, labelfile = 'labels_new.txt')
testset1 = Markers(train=False, transform=transform, labelfile = 'testlabels_1.txt')
testset0 = Markers(train=False, transform=transform, labelfile = 'testlabels_0.txt')

trainloader = data.DataLoader(trainset, batch_size=32,
                                          shuffle=True,
                                          num_workers=2)
testloader1 = data.DataLoader(testset1, batch_size=2,
                                          shuffle=False,
                                          num_workers=2)
testloader0 = data.DataLoader(testset0, batch_size=2,
                                          shuffle=False,
                                          num_workers=2)





net = Net(fSize=32)
optimiser = optim.Adam(net.parameters(), lr=1e-4)


for epoch in range(150):

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

	test1_correct = 0
	for i, data in enumerate(testloader1):
		x, labels = data
		x = Variable(x)
		preds = net.forward(x)
		for k in range(len(preds)):
			if abs(preds[k].data.numpy() - labels[k]) < 0.5:
				test1_correct += 1

	test1_accurary = test1_correct / testset1.__len__()
	test0_correct = 0
	for i, data in enumerate(testloader0):
		x, labels = data
		x = Variable(x)
		preds = net.forward(x)
		for k in range(len(preds)):
			if abs(preds[k].data.numpy() - labels[k]) < 0.5:
				test0_correct += 1

	test0_accurary = test0_correct / testset0.__len__()

	print('%d turnover rate  %.5f' % (epoch, test1_accurary))
	print('%d fp rate  %.5f' % (epoch, 1-test0_accurary))

#net.save_params(os.getcwd())
