# -*- coding: utf-8 -*-
import os, torch, glob
import numpy as np
from torch.autograd import Variable
from PIL import Image
from torchvision import models, transforms
import torch.nn as nn
import tensorflow as tf
import json
import matplotlib.pyplot as plt
import copy
import os
from lxml import etree
import requests
import json
from bs4 import BeautifulSoup
import math
import random

base_url = "http://m.mafengwo.cn"
result_dir = os.path.join(os.path.dirname(__file__), "../static/demo_result").replace("\\", "/")#"C:/Users/Adlijiang Abulikemu/Desktop/ClothesRecommend/backend/app/static/demo_result"
train_result_dir = os.path.join(os.path.dirname(__file__), "demo_train_result").replace("\\", "/")

def spider(key, image_num):
    url = "https://www.mafengwo.cn/ajax/ajax_any_index.php"
    querystring = {"sAction":"getSearchCity","sKey":key}
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "www.mafengwo.cn",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive"
    }

    response = requests.get(url, headers=headers, params=querystring)
    response.encoding = "utf-8"
    data = json.loads(response.text)
    id = data["payload"]["data"][0]["id"]
    print ("id: %d" % id)

    page = 1
    num = 0
    while (num < image_num):
        url = "https://pagelet.mafengwo.cn/note/pagelet/recommendNoteApi"
        querystring = {"params":"{\"type\":2,\"objid\":%s,\"page\":%d,\"ajax\":1,\"retina\":1}" % (id, page)}
        headers["Host"] = "pagelet.mafengwo.cn"

        response = requests.request("GET", url, headers=headers, params=querystring)
        response.encoding = "utf-8"
        data = json.loads(response.text)
        html = data["data"]["html"]

        soup = BeautifulSoup(html, features="lxml")
        tn_list = soup.find_all("div", "tn-image")

        for item in tn_list:
            url = base_url + item.a['href']
            print (url)

            headers["Host"] = "www.mafengwo.cn"
            response = requests.request("GET", url, headers=headers)

            # find img
            soupp = BeautifulSoup(response.text, features="lxml")
            img_url_list = soupp.find_all("img", "_j_lazyload _j_needInitShare")
            for (index, item) in enumerate(img_url_list):
                img_url = item["data-src"]
                print (img_url)
                res = requests.request("GET", img_url)

                if not os.path.exists(result_dir):
                    os.path.mkdir(result_dir)

                if res.content:
                    with open("%s/%s.jpg" % (result_dir, item["data-pid"]), "wb") as f:
                        f.write(res.content)
                        num += 1
                        print (num)
                if (num >= image_num):
                    return


# import shutil
data_dir = result_dir
features_dir = result_dir
jd_dataset_dir = os.path.join(os.path.dirname(__file__), "../static/wqJD_20190120").replace("\\", "/")#'C:\\Users\\Adlijiang Abulikemu\\Desktop\\ClothesRecommend\\backend\\app\\static\\wqJD_20190120\\'
img_result_base_dir = "http://localhost/static/wqJD_20190120/"

# shutil.copytree(data_dir, os.path.join(features_dir, data_dir[2:]))
DIST_MAX = 9999999999
THRESHOLD = 0.9

def random_n(T: int, num: int):
    '''
    从[0, T)中随机抽取num个整数
    :return: 一个list，包含num个整数
    '''
    t = []
    for i in range(T):
        t.append(i)
    random.shuffle(t)
    return t[0: num]

def euclid_distance(dot1: list, dot2: list, dimen: int):
    '''
    计算两点间欧几里得距离
    :param dot1: 第一个点
    :param dot2: 第二个点
    :param dimen: 维度
    :return: 距离
    '''
    t = 0
    for i in range(dimen):
        t += math.pow(dot1[i] - dot2[i], 2)
    return math.sqrt(t)

def square_error(input_dots: list, dimen: int, mid_pos:list, classify_list: list):
    '''
    :param input_dots: 输入的若干个点
    :param dimen: 维数
    :param mid_pos: 所有簇中心的位置
    :param classify_list: 每个点的分类类别
    :return: 总距离和
    '''
    t = 0
    for i in range(len(input_dots)):
        t += euclid_distance(input_dots[i], mid_pos[classify_list[i]], dimen)
    return t

def k_means(input_dots: list, dimen: int, k: int):
    '''
    k_means算法
    :param input_dots: 输入的所有点的集合
    :param dimen: 点的维数
    :param k: 需要聚类的类别个数
    :return: 聚类的k个点坐标
    '''
    # 任意抽取k个对象作为初始簇中心
    mid_list = random_n(len(input_dots), k)
    mid_pos = [copy.deepcopy(input_dots[i]) for i in mid_list]
    dist_list = [0] * len(input_dots)
    dist_total = DIST_MAX
    # 循环更新每个簇中心的位置
    while True:
        # 计算每个点到每个簇中心的距离，进行分类
        for i in range(len(input_dots)):
            t = DIST_MAX
            for j in range(k):
                e_dist = euclid_distance(input_dots[i], mid_pos[j], dimen)
                if e_dist < t:
                    t = e_dist
                    dist_list[i] = j
        # 重新计算每个簇的中心
        #mid_pos = [[0] * dimen] * k
        mid_cnt = [1] * k
        for i in range(len(input_dots)):
            mid_cnt[dist_list[i]] += 1
            for d in range(dimen):
                mid_pos[dist_list[i]][d] += input_dots[i][d]
        for i in range(k):
            for d in range(dimen):
                mid_pos[i][d] /= mid_cnt[i]
        new_dist_total = square_error(input_dots, dimen, mid_pos, classify_list=dist_list)
        if new_dist_total / dist_total > THRESHOLD:
            break
        else:
            dist_total = new_dist_total
        '''gplt.title("test")
        np_dot_list = numpy.asarray(input_dots).transpose()
        plt.plot(np_dot_list[0], np_dot_list[1], 'ob')
        np_dot_list = numpy.asarray(mid_pos).transpose()
        print(mid_pos)
        plt.plot(np_dot_list[0], np_dot_list[1], 'or')
        plt.show()'''
    return mid_pos


def k_mediods(input_dots: list, dimen: int, k: int):
    '''
    k_mediods算法
    :param input_dots: 输入的所有点的集合
    :param dimen: 点的维数
    :param k: 需要聚类的类别个数
    :return: 聚类的k个点坐标
    '''

def nearest(input_dots: list, test_dot: list, dimen: int):
    '''
    查找最近的点
    :param input_dots:
    :param test_dot:
    :param k:
    :return:
    '''
    dist = DIST_MAX
    ret_dot = []
    for dot in input_dots:
        temp_dist = euclid_distance(dot, test_dot, dimen)
        if temp_dist < dist:
            ret_dot = dot
    return ret_dot

def nearest(input_dots: dict, test_dot: list, dimen: int):
    '''
    查找最近的点
    :param input_dots:
    :param test_dot:
    :param k:
    :return:
    '''
    dist = DIST_MAX
    ret_dot_index = []
    for dot_index in input_dots:
        temp_dist = euclid_distance(input_dots[dot_index], test_dot, dimen)
        if temp_dist < dist:
            ret_dot_index = dot_index
            dist = temp_dist
    return ret_dot_index

def extractor(img_path, saved_path, net, use_gpu):
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor()]
    )
    try:
        img = Image.open(img_path)
        img = img.convert("RGB")
        # print(img.size)
        img = transform(img)
        # print(img.shape)
    except Exception as e:
        f = open('error.txt', 'a')
        f.write(img_path + '\n')
        f.close()
        print(img_path)
        return

    x = Variable(torch.unsqueeze(img, dim=0).float(), requires_grad=False)
    if use_gpu:
        x = x.cuda()
        net = net.cuda()
    y = net(x).cpu()
    y = y.data.numpy()
    y = np.squeeze(y)
    np.savetxt(saved_path, y, delimiter=',')
    print(saved_path)


def get_demo_result(key, image_num=15):
    # delele all files in ./demo_result and spider
    for filename in os.listdir(result_dir):
        os.remove(result_dir + '/' + filename)
    spider(key, image_num)

    extensions = ['jpg', 'jpeg', 'JPG', 'JPEG']

    filenames = os.listdir(data_dir)
    files_list = [data_dir + '/' + filename for filename in filenames if True in [filename.endswith(ex) for ex in extensions]]
    '''
    sub_dirs = [x[0] for x in os.walk(data_dir) ]
    sub_dirs = sub_dirs[1:]
    for sub_dir in sub_dirs:
        for extention in extensions:
            file_glob = os.path.join(sub_dir, '*.' + extention)
            files_list.extend(glob.glob(file_glob))
    '''
    resnet = models.resnet50(pretrained=True)
    # print(resnet)
    # resnet.fc = nn.Linear(2048, 2048)
    # torch.nn.init.eye(resnet.fc.weight)
    # resnet = models.resnet152(pretrained=True)
    modules = list(resnet.children())[:-1]  # delete the last fc layer.
    convnet = nn.Sequential(*modules)
    # print(convnet)

    for param in convnet.parameters():
        param.requires_grad = False

    use_gpu = torch.cuda.is_available()
    i = 0
    print(len(files_list))
    for x_path in files_list:
        i += 1
        # print(x_path)
        # fx_path = os.path.join(features_dir, x_path[2:].split('/')[-1] + '.txt')
        fx_path = features_dir + '/' + x_path[2:].split('/')[-1] + '.txt'
        if os.path.exists(fx_path):
            continue
        if i % 100 == 0:
            print(i)
        extractor(x_path, fx_path, convnet, use_gpu)
        # break
    saver = tf.train.import_meta_graph(os.path.join(train_result_dir, 'fn2048_2.meta').replace("\\", "/"))
    sess = tf.Session()
    saver.restore(sess, tf.train.latest_checkpoint(train_result_dir))
    dots = []
    for filename in os.listdir(features_dir):
        if filename.endswith('.txt'):
            pred = sess.run('full2:0', feed_dict={'input:0':[[float(s.strip()) for s in open(features_dir + '/'+filename,'r').readlines()]],'keep_prob:0':1.0})
            dots.append(pred.tolist()[0])
    print(dots)
    array = np.asarray(dots).transpose()
    plt.plot(array[0], array[1], 'ob')
    mid_dots = k_means(dots, 2, 1)
    array = np.asarray(mid_dots).transpose()
    plt.plot(array[0], array[1], 'or')
    fmap_dict = json.loads(open(os.path.join(train_result_dir, 'feature_map.txt').replace("\\", "/"), 'r').read())
    print(mid_dots)
    indexs=[]
    for dot in mid_dots:
        index = nearest(fmap_dict, dot, 2)
        n_dot = fmap_dict[index]
        plt.plot(n_dot[0], n_dot[1], 'oy')
        print(index)
        indexs.append(index)
    '''
    plt.xticks(np.arange(-1.0, 1.0, 0.2))
    plt.yticks(np.arange(-1.0, 1.0, 0.2))
    plt.show()
    '''
    return [img_result_base_dir+('%s/%s_outfit_0.jpg' % (s,s)) for s in indexs]

if __name__ == '__main__':
    print(get_demo_result('迪拜'))
