# ------------------------------------------------------------------------------
# This class represents different classification models.
# ------------------------------------------------------------------------------

import torch.nn as nn
import torch
from mp.models.model import Model
import torchvision.models as models

<<<<<<< HEAD
# Sigmoid layers are important for the BCELoss, to get multi-hot vectors
# for multi classification task.

=======
>>>>>>> 6192c2bfa88c3375ba21cd95f262a03613b79546
class AlexNet(Model):
    r"""This class represents the AlexNet for image classification."""
    def __init__(self, num_labels):
        super(AlexNet, self).__init__()
        self.alexnet = models.alexnet(pretrained=True)
        classifier_input = self.alexnet.classifier[-1].in_features
        self.alexnet.classifier[-1] = nn.Linear(classifier_input, num_labels)
        self.alexnet.eval()
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, x):
        # Reshape input based on batchsize
        yhat = self.alexnet(x)
        yhat = self.sigmoid(yhat)
        return yhat

class VGG19BN(Model):
    r"""This class represents the VGG19 for image classification with
        Batch normalization."""
    def __init__(self, num_labels):
        super(VGG19BN, self).__init__()
        self.vgg = models.vgg19_bn(pretrained=True)
        self.softmax = nn.Softmax(dim=1)
        self.relu = nn.ReLU(inplace=True)
        self.do = nn.Dropout(p=0.5)
        self.lin1 = nn.Linear(1000, num_labels)
        
    def forward(self, x):
        # Reshape input based on batchsize
        yhat = self.vgg(x)
        yhat = yhat.view(yhat.size(0), -1)
        yhat = self.lin1(yhat)
        return yhat

<<<<<<< HEAD
class ResNet(Model):
    r"""This class represents the ResNet for image classification."""
    def __init__(self, num_labels):
        super(ResNet, self).__init__()
        self.resnet = models.resnet18(pretrained=True)
        classifier_input = self.resnet.fc.in_features
        self.resnet.fc = nn.Linear(classifier_input, num_labels)
        self.resnet.eval()
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, x):
        # Reshape input based on batchsize
        yhat = self.resnet(x)
        yhat = self.sigmoid(yhat)
        return yhat

class CNN_Net2D(Model):   
    r"""This class represents a CNN for 2D image classification,
    detecting tools in video frames.
    The input image needs to have the size 3x224x224. Otherwise the
=======
class CNN_Net2D(Model):   
    r"""This class represents a CNN for 2D image classification,
    detecting CT artefacts in CT slices.
    The input image needs to have the size 299x299. Otherwise the
>>>>>>> 6192c2bfa88c3375ba21cd95f262a03613b79546
    number of input features for the Linear layer needs to be changed!"""
    def __init__(self, num_labels):
        super(CNN_Net2D, self).__init__()
        self.cnn_layers = nn.Sequential(
            # Defining a first 2D convolution layer
<<<<<<< HEAD
            nn.Conv2d(3, 4, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(4),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),      #dim: 4x112x112
=======
            nn.Conv2d(1, 4, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(4),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
>>>>>>> 6192c2bfa88c3375ba21cd95f262a03613b79546
            # Defining a second 2D convolution layer
            nn.Conv2d(4, 8, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(8),
            nn.ReLU(inplace=True),
<<<<<<< HEAD
            nn.MaxPool2d(kernel_size=2, stride=2),      #dim: 8x56x56
=======
            nn.MaxPool2d(kernel_size=2, stride=2),
>>>>>>> 6192c2bfa88c3375ba21cd95f262a03613b79546
            # Defining a third 2D convolution layer
            nn.Conv2d(8, 8, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(8),
            nn.ReLU(inplace=True),
<<<<<<< HEAD
            nn.MaxPool2d(kernel_size=2, stride=2),      #dim: 8x28x28
=======
            nn.MaxPool2d(kernel_size=2, stride=2),
>>>>>>> 6192c2bfa88c3375ba21cd95f262a03613b79546
            # Defining a forth 2D convolution layer
            nn.Conv2d(8, 8, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(8),
            nn.ReLU(inplace=True),
<<<<<<< HEAD
            nn.MaxPool2d(kernel_size=2, stride=2)       #dim: 8x14x14
=======
            nn.MaxPool2d(kernel_size=2, stride=2)
>>>>>>> 6192c2bfa88c3375ba21cd95f262a03613b79546
        )

        self.linear_layers = nn.Sequential(
            # Output shape of cnn_layers
<<<<<<< HEAD
            nn.Linear(8 * 14 * 14, num_labels)
        )

        self.sigmoid = nn.Sigmoid()
=======
            nn.Linear(8 * 18 * 18, num_labels)
        )

    # Defining the forward pass    
    def forward(self, x):
        print(x.size())
        yhat = self.cnn_layers(x)
        yhat = yhat.view(yhat.size(0), -1)
        yhat = self.linear_layers(yhat)
        return yhat

class CNN_Net3D(Model):   
    r"""This class represents a CNN for 3D image/video classification,
    detecting CT artefacts in CT slices.
    The input image needs to have the size 480x854x3. Otherwise the
    number of input features for the Linear layer needs to be changed!
    
    TODO: Change the number of layers based on input as well as linear layer!"""
    def __init__(self, num_labels):
        super(CNN_Net3D, self).__init__()
        self.cnn_layers = nn.Sequential(
            # Defining a first 3D convolution layer
            nn.Conv3d(1, 4, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm3d(4),
            nn.ReLU(inplace=True),
            nn.MaxPool3d(kernel_size=2, stride=2),
            # Defining a second 3D convolution layer
            nn.Conv3d(4, 8, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm3d(8),
            nn.ReLU(inplace=True),
            nn.MaxPool3d(kernel_size=2, stride=2),
            # Defining a third 3D convolution layer
            nn.Conv3d(8, 8, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm3d(8),
            nn.ReLU(inplace=True),
            nn.MaxPool3d(kernel_size=2, stride=2),
            # Defining a forth 3D convolution layer
            nn.Conv3d(8, 8, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm3d(8),
            nn.ReLU(inplace=True),
            nn.MaxPool3d(kernel_size=2, stride=2)
        )

        self.linear_layers = nn.Sequential(
            # Output shape of cnn_layers
            nn.Linear(8 * 18 * 18, num_labels)
        )
>>>>>>> 6192c2bfa88c3375ba21cd95f262a03613b79546

    # Defining the forward pass    
    def forward(self, x):
        yhat = self.cnn_layers(x)
<<<<<<< HEAD
        yhat = yhat.view(yhat.size(0), -1)
        yhat = self.linear_layers(yhat)
        yhat = self.sigmoid(yhat)
=======
        print(yhat.size())
        yhat = yhat.view(yhat.size(0), -1)
        yhat = self.linear_layers(yhat)
>>>>>>> 6192c2bfa88c3375ba21cd95f262a03613b79546
        return yhat