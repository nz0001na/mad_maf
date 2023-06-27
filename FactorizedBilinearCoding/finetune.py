'''
env: env_FR_27
'''
# encoding:utf-8
import torch
import torch.optim as optim
import torchvision.transforms as transforms
import torch.nn as nn
from torch.autograd import Variable
import os
import math
from config import opt
import time
from data.dataset import MyDataset
from models.FBC import FBC  #
import argparse
import sys
import numpy as np
import scipy.io as sio

# li = ['A_set_1_shot_test','A_set_1_shot_train',
#     'A_set_5_shot_test','A_set_5_shot_train',
#     'B_set_1_shot_test', 'B_set_1_shot_train',
#     'B_set_5_shot_test', 'B_set_5_shot_train',
#     'C_set_1_shot_test', 'C_set_1_shot_train',
#     'C_set_5_shot_test','C_set_5_shot_train']
acc_list = [0.0]
loss_list = [0.0]
criterion = nn.CrossEntropyLoss()
# name = li[11]
dst_path = './feature/mad-fingerprinting/'
if os.path.exists(dst_path) is False:
    os.makedirs(dst_path)

# dst_path2 = './feature/mad-fingerprinting/ours/'
# if os.path.exists(dst_path2) is False:
#     os.makedirs(dst_path2)

name = '5_self_test'  #

def train(epoch, lr):
    print('model_name_pre:',args.model_name_pre)
    print('bs',args.train_bs)
    print('SC beta:', args.BETA)
    print('rank:',args.RANK_ATOMS)
    print('num cluster:',args.NUM_CLUSTER)
    print('save_low_bound:',args.save_low_bound)
    print('weight_decay:',args.weight_decay)
    if args.DTD:
        print('dataset:','DTD')
    # elif args.Aircraft:
    #     print('dataset:','Aircraft')
    # elif args.CUB:
    #     print('dataset:','CUB')
    # elif args.INDOOR:
    #     print('dataset:','INDOOR')
    # elif args.MINC2500:
    #     print('dataset:','MINC2500')
    elif args.MAD:
        print('dataset:','MAD')
    epoch_start = time.time()

    features_lr = lr * 0.1
    if features_lr <= 0.0001:
        features_lr = 0.0001
    optimizer = optim.SGD(
        [
        {'params': model.features.parameters(), 'lr':features_lr},
        {'params': model.Linear_dataproj_k.parameters(), 'lr': lr},
        {'params': model.Linear_dataproj2_k.parameters(), 'lr': lr},
        {'params': model.Linear_predict.parameters(),'lr':lr},
        ], 
        lr=lr, momentum=0.9, weight_decay=args.weight_decay) 

    model.train()
    start = time.time()
    running_loss = 0.0

    train_bs = args.train_bs
    train_len = len(trainset)
    for batch_idx, (data, data2, target) in enumerate(trainloader):
        if (batch_idx+1) * train_bs > train_len:
            break
        data = Variable(data)
        data2 = Variable(data2)
        target = Variable(target)
        data, data2, target = data.cuda(), data2.cuda(), target.cuda()
        optimizer.zero_grad()
        bi_fea, output = model(data, data2)
        loss = criterion(output, target)

        loss.backward()
        running_loss += loss.data.item()
        optimizer.step()
        if batch_idx % (args.train_print_freq/args.train_bs) == 0 and batch_idx != 0:
            loss_tmp = running_loss / (args.train_print_freq/args.train_bs) #div the n of batch
            interval = time.time() - start
            start = time.time()
            print('Epoch:{}[{}/{} ]\tLoss:{:.6f}\tLR:{}\tbeta:{}\ttime:{:.2f}'.format(
                epoch, batch_idx * len(data), train_len, loss_tmp, lr,  model.sc.beta, interval/60))
            running_loss = 0.0
    epoch_end = time.time()
    tmp = (epoch_end - epoch_start) / 60
    print('train time:{:.4f} min'.format(tmp))

def test(epoch, lr):
    model.eval()
    test_loss = 0
    correct = 0
    start = time.time()
    test_bs = args.test_bs
    test_len = len(testset)
    test_feature = []
    test_label = []
    for batch_idx, (data, data2, target) in enumerate(testloader):
        if (batch_idx+1) * test_bs > test_len:
            break
        # print(batch_idx)
        data = Variable(data)
        data2 = Variable(data2)
        target = Variable(target)
        data, data2, target = data.cuda(), data2.cuda(), target.cuda()
        bi_fea, output = model(data, data2) # save test fea
        # save bi_fea, target
        fea = bi_fea.cpu().detach().numpy()
        label = target.cpu().detach().numpy()
        if len(test_feature) == 0:
            test_feature = fea
            test_label = label
        test_feature = np.concatenate((test_feature, fea), axis=0)
        test_label = np.concatenate((test_label, label), axis=0)

        test_loss += criterion(output, target).data.item()
        pred = output.data.max(1, keepdim=True)[1]
        correct += pred.eq(target.data.view_as(pred)).cpu().sum()

    # dict = {}
    # dict['test_feature'] = np.asarray(test_feature)
    # dict['test_label'] = np.asarray(test_label)
    # sio.savemat(dst_path + str(epoch) + '_' + db + '.mat', dict)
    # print(np.shape(np.asarray(test_feature)))
    # print(np.shape(np.asarray(test_label)))

    test_loss = test_loss / (test_len / args.test_bs)   
    loss_list.append(round(test_loss, 4))
    acc = 100.0 * float(correct) / test_len
    acc = round(acc, 4)
    interval = time.time() - start
    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.2f}%)\ttime:{:.2f}\n'.format(
        test_loss , correct, test_len, acc, interval/60))

    if os.path.exists('./tmp/') is False: os.makedirs('./tmp/')
    model_name = './tmp/' + str(epoch) + '_' + args.model_name_pre + str(acc) + '_lr_' + str(lr) + '.pth'
    acc_max = max(acc_list)
    if acc > acc_max and acc > args.save_low_bound:
        torch.save(model.state_dict(), model_name)
        print('i have saved the model')

    acc_list.append(acc)
    acc_max = max(acc_list)
    print('max acc:', acc_max)
    print('acc list:', acc_list)
    print('loss list:', loss_list)


def test_sample():
    print('Ours.......')
    model.eval()
    # test_loss = 0
    correct = 0
    start = time.time()
    test_bs = args.test_bs
    test_len = len(testset)
    test_feature = []
    test_label = []
    for batch_idx, (data, data2, target) in enumerate(testloader):
        if (batch_idx+1) * test_bs > test_len:
            break
        # print(batch_idx)
        data = Variable(data)
        data2 = Variable(data2)
        target = Variable(target)
        data, data2, target = data.cuda(), data2.cuda(), target.cuda()
        bi_fea, output = model(data, data2) # save test fea
        # save bi_fea, target
        fea = bi_fea.cpu().detach().numpy()
        label = target.cpu().detach().numpy()
        if len(test_feature) == 0:
            test_feature = fea
            test_label = label
        test_feature = np.concatenate((test_feature, fea), axis=0)
        test_label = np.concatenate((test_label, label), axis=0)

        # test_loss += criterion(output, target).data.item()
        pred = output.data.max(1, keepdim=True)[1]
        correct += pred.eq(target.data.view_as(pred)).cpu().sum()

    dict = {}
    dict['feature'] = np.asarray(test_feature)
    dict['label'] = np.asarray(test_label)
    # print(np.shape(np.asarray(test_feature)))
    sio.savemat(dst_path + name + '.mat', dict)
    print(np.shape(np.asarray(test_feature)))
    print(np.shape(np.asarray(test_label)))

    # test_loss = test_loss / (test_len / args.test_bs)
    # loss_list.append(round(test_loss, 4))
    acc = 100.0 * float(correct) / test_len
    acc = round(acc, 4)
    interval = time.time() - start
    print('\nTest set: Accuracy: {}/{} ({:.2f}%)\ttime:{:.2f}\n'.format(
        correct, test_len, acc, interval/60))

    # if os.path.exists('./tmp/') is False: os.makedirs('./tmp/')
    # model_name = './tmp/' + str(epoch) + '_' + args.model_name_pre + str(acc) + '_lr_' + str(lr) + '.pth'
    # acc_max = max(acc_list)
    # if acc > acc_max and acc > args.save_low_bound:
    #     torch.save(model.state_dict(), model_name)
    #     print('i have saved the model')

    # acc_list.append(acc)
    # acc_max = max(acc_list)
    # print('max acc:', acc_max)
    # print('acc list:', acc_list)
    # print('loss list:', loss_list)

def parse_args(*args):
    parser = argparse.ArgumentParser()

    parser.add_argument('-DTD','--DTD', default=opt.DTD)
    parser.add_argument('-CUB','--CUB', default=opt.CUB)
    parser.add_argument('-INDOOR','--INDOOR', default=opt.INDOOR)
    parser.add_argument('-MINC2500','--MINC2500', default=opt.MINC2500) #
    parser.add_argument('-MAD', '--MAD', default=True)
    parser.add_argument('-data_path','--data_path', default=opt.data_path) #
    parser.add_argument('-train_txt_path','--train_txt_path', default=opt.train_txt_path) #
    parser.add_argument('-test_txt_path','--test_txt_path', default=opt.test_txt_path) #
    parser.add_argument('-class_num','--class_num', default=opt.class_num) #
    parser.add_argument('-res_plus','--res_plus', type=int, default=opt.res_plus)
    parser.add_argument('-res','--res', type=int, default=opt.res)
    parser.add_argument('-lr','--lr', type=float, default=0.01)
    parser.add_argument('-lr_scale','--lr_scale', type=float, default=opt.lr_scale)
    parser.add_argument('-train_bs','--train_bs', type=int, default=opt.train_bs)
    parser.add_argument('-device','--gpu_device', default=opt.gpu_device)
    parser.add_argument('-rank','--RANK_ATOMS', type=int, default=1) # opt.RANK_ATOMS
    parser.add_argument('-k','--NUM_CLUSTER', type=int, default=2048) # opt.NUM_CLUSTER
    parser.add_argument('-beta','--BETA', type=float, default=0.001) # opt.BETA
    parser.add_argument('-model_name_pre','--model_name_pre', default=opt.model_name_pre)
    parser.add_argument('-model_path','--model_path', default=opt.model_path) #
    parser.add_argument('-save_low_bound','--save_low_bound', type=float, default=opt.save_low_bound)
    parser.add_argument('-weight_decay','--weight_decay', type=float, default=5e-4)
    parser.add_argument('-train_print_freq','--train_print_freq', type=int, default=opt.train_print_freq)
    parser.add_argument('-test_bs','--test_bs', type=int, default=opt.test_bs)
    parser.add_argument('-test_epoch','--test_epoch', type=int, default=opt.test_epoch)
    parser.add_argument('-pretrained','--pretrained', default=opt.pretrained)
    parser.add_argument('-pre_model_path','--pre_path', default=opt.pre_path)
    parser.add_argument('-model_name','--model_name', default=opt.model_name) #
    parser.add_argument('-use_gpu','--use_gpu', default=opt.use_gpu)
    parser.add_argument('-max_epoches','--max_epoches', type=int, default=opt.max_epoches)

    args = parser.parse_args()
    return args

def main(argv):
    global args 
    global model
    args = parse_args(argv)
    os.environ["CUDA_VISIBLE_DEVICES"] = '2' # args.gpu_device
    if args.model_name == 'FBC':
        print('model:','FBC')
        model = FBC()
    else:
        print('model error')
    model.cuda()

    if args.model_path:
        print('i am load model', args.model_path)
        pre_model = torch.load(args.model_path)
        model_dict = model.state_dict()
        pre_dict = {k:v for k, v in pre_model.items() if k in model_dict}
        print('pre dict len:',len(pre_dict))
        model_dict.update(pre_dict)
        model.load_state_dict(model_dict)
    elif args.pretrained:
        print('l am loading pre model', args.pre_path)
        pre_model = torch.load(args.pre_path)
        model_dict = model.state_dict()
        pre_dict = {k:v for k, v in pre_model.items() if k in model_dict}
        print('pre dict len:',len(pre_dict))
        model_dict.update(pre_dict)
        model.load_state_dict(model_dict)
    else:
        for m in model.modules():
            if isinstance(m, nn.Conv2d):
                n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                m.weight.data.normal_(0, math.sqrt(2. / n))
            elif isinstance(m, nn.BatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()

    if True:
        train_txt_path = args.train_txt_path
        global trainset
        trainset = MyDataset(train_txt_path, transform=transforms.Compose([
                                                        #transforms.Scale((args.res_plus,args.res_plus)),
                                                        transforms.Scale(224),
                                                        #transforms.RandomHorizontalFlip(),
                                                        #transforms.RandomCrop(args.res),
                                                        transforms.ToTensor(),
                                                        transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))
                                                        ]))
        train_len = len(trainset)
        print('train_len:',train_len)
        train_bs = args.train_bs
        global trainloader
        trainloader = torch.utils.data.DataLoader(trainset, batch_size=train_bs, shuffle=True)
        test_txt_path = args.test_txt_path
        global testset
        testset = MyDataset(test_txt_path, transform=transforms.Compose([
                                                        #transforms.Scale((args.res_plus,args.res_plus)),
                                                        transforms.Scale(224),
                                                        #transforms.CenterCrop(args.res),
                                                        transforms.ToTensor(),
                                                        transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))
                                                        ]))
        test_len = len(testset)
        print('test_len:',test_len)
        test_bs = args.test_bs
        global testloader
        testloader = torch.utils.data.DataLoader(testset, batch_size=test_bs, shuffle=False)

    lr = args.lr
    mode = False     # 1 : train 0: test
    if mode:
        for epoch in range(1, args.max_epoches):
            if epoch in opt.lr_freq_list:
                lr = lr * args.lr_scale
                lr = max(lr, 0.0001)
            train(epoch, lr)
            if epoch % args.test_epoch == 0:
                test(epoch, lr)
    else:
        test_sample()

if __name__ == '__main__':
    main(sys.argv[1:])
    



        