#coding:utf-8
from torch import nn
import torch
from .BasicModule import BasicModule
import torch.nn.functional as F
import math
import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__)+os.path.sep+".."))
# from ..config import opt
import scipy.io as sio
from torch.autograd import Variable
from torch.nn import Parameter as Parameter
from .SC import SC
import torchvision

RANK_ATOMS = 1
NUM_CLUSTER = 4096
down_chennel = 512  # 2048
res = 224
BETA = 0.001
class_num = 9

class FBC(BasicModule):
    def __init__(self):  
        super(FBC, self).__init__()
        self.features = torchvision.models.vgg16(pretrained=True).features
        # self.features = torchvision.models.resnet50(pretrained=True).features
        self.features = torch.nn.Sequential(*list(self.features.children())[:-1])  # Remove pool5.

        self.device=torch.device("cuda")
        self.output_dim = self.JOINT_EMB_SIZE = RANK_ATOMS * NUM_CLUSTER #20*2048
        self.input_dim = down_chennel

        self.Linear_dataproj_k = nn.Linear(down_chennel, self.JOINT_EMB_SIZE)
        self.Linear_dataproj2_k = nn.Linear(down_chennel, self.JOINT_EMB_SIZE)

        self.Linear_predict = nn.Linear(NUM_CLUSTER, class_num)

        self.sc = SC(beta=BETA)
        if res == 224:
            self.Avgpool = nn.AvgPool1d(kernel_size=196)
        elif res == 448:
            self.Avgpool = nn.AvgPool1d(kernel_size=784)

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.xavier_normal_(m.weight.data,)
                m.bias.data.zero_()
            elif isinstance(m, nn.BatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()
            elif isinstance(m, nn.Linear):
                nn.init.xavier_normal_(m.weight.data)
                m.bias.data.zero_()
        

    def forward(self, x1, x2):
        x1 = self.features(x1)
        x2 = self.features(x2)
        bs, c, w, h = x1.shape[0:4]
        # bswh = bs*w*h
        x1 = x1.permute(0,2,3,1)
        x1= x1.contiguous().view(-1,c)
        x2 = x2.permute(0,2,3,1)
        x2= x2.contiguous().view(-1,c)

        x1 = self.Linear_dataproj_k(x1)
        x2 = self.Linear_dataproj2_k(x2)
        bi = x1.mul(x2)

        bi = bi.view(-1, 1, NUM_CLUSTER, RANK_ATOMS)
        bi = torch.squeeze(torch.sum(bi, 3))
        bi = self.sc(bi)
        bi = bi.view(bs, h*w, -1)
        bi = bi.permute(0,2,1)                                      
        bi = torch.squeeze(self.Avgpool(bi))                   

        bi = torch.sqrt(F.relu(bi)) - torch.sqrt(F.relu(-bi))      
        bi = F.normalize(bi, p=2, dim=1) #[bs, 512]

        y = self.Linear_predict(bi)  #[bs,2]
        return bi, y


if __name__ == '__main__':
    # model = torch.load('tmp/FBC94.0_lr_0.01.pth')
    # model.eval()


    print(1)

