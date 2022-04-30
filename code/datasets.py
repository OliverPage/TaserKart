#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 15:23:10 2022

@author: oliverpage
"""
import torchvision.transforms as transforms
import torchvision.datasets as datasets
from torch.utils.data import DataLoader
# batch size
BATCH_SIZE = 64

# the training transforms
train_transform = transforms.Compose([
    transforms.Resize(224),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomVerticalFlip(p=0.5),
    transforms.GaussianBlur(kernel_size=(5, 9), sigma=(0.1, 5)),
    transforms.RandomRotation(degrees=(30, 70)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.5, 0.5, 0.5],
        std=[0.5, 0.5, 0.5]
    )
])
# the validation transforms
valid_transform = transforms.Compose([
    transforms.Resize(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.5, 0.5, 0.5],
        std=[0.5, 0.5, 0.5]
    )
])

# training dataset
train_dataset = datasets.ImageFolder(
    root='TaserKart-main/data/train',
    transform=train_transform
)
# validation dataset
valid_dataset = datasets.ImageFolder(
    root='TaserKart-main/data/valid',
    transform=valid_transform
)

# Get subset of images to faster training
number_of_images = 100
train_dataset.samples = [train_dataset.samples[idx] for idx in range(number_of_images)]
valid_dataset.samples = [valid_dataset.samples[idx] for idx in range(number_of_images)]


# training data loaders
train_loader = DataLoader(
    train_dataset, batch_size=BATCH_SIZE, shuffle=True,
    num_workers=4, pin_memory=True
)
# validation data loaders
valid_loader = DataLoader(
    valid_dataset, batch_size=BATCH_SIZE, shuffle=False,
    num_workers=4, pin_memory=True
)