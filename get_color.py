from sklearn.cluster import KMeans
from collections import Counter
from matplotlib import pyplot as plt
import cv2
# Utility function, rgb to hex
import math
import numpy as np
def rgb2hex(rgb):
    hex = "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
    return hex
# print(rgb2hex([255, 0, 0]))
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv//3], 16) for i in range(0, lv, lv//3))
def distance(c1, c2) :
    (r1, g1, b1) = c1
    (r2, g2, b2) = c2
    return math.sqrt((r1 - r2) * 2 + (g1 - g2) * 2 + (b1 - b2) ** 2)
def plot_image_info(path, k=6) :
    # load image
    img_bgr = cv2.imread(path)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    # resize image to speed up processing time
    resized_img_rgb = cv2.resize(img_rgb, (64, 64), interpolation=cv2.INTER_AREA)
    # reshape the image to be a list of pixels
    img_list = resized_img_rgb.reshape((resized_img_rgb.shape[0] * resized_img_rgb.shape[1], 3))
    # cluster the pixels and assign labels
    clt = KMeans(n_clusters=k)
    labels = clt.fit_predict(img_list)
    # count labels to find most popular
    label_counts = Counter(labels)
    # subset out most popular centroid
    center_colors = list(clt.cluster_centers_)
    # print('center_colors:',center_colors)
    ordered_colors = [center_colors[i] / 255 for i in label_counts.keys()]
    color_labels = [rgb2hex(ordered_colors[i] * 255) for i in label_counts.keys()]
    # print('label_counts:',label_counts.values()) #產生色碼
    # print('color_labels:',color_labels)
    # print('ordered_colors:',ordered_colors)
    # plots
    plt.figure(figsize=(14, 8))
    plt.subplot(221)
    plt.imshow(img_rgb)
    plt.axis('off')
    #計算比率
    def percentage(part, whole) :
        return 100 * float(part) / float(whole)
    colorDict = dict()
    #由大到小排列, 取出前三樣圖片, 組成csv
    # print(label_counts.values())
    j=0
    # for i in label_counts.values():
    for i,data in enumerate(label_counts.keys()):
        #無任一顏色超過30%, 取第一筆顏色 並尋找其同色系增強視覺
        #有一個主配色: 僅一種顏色高達30%, 尋找其互補色
        #有兩個主配色: 兩種顏色或以上高達30% ??等待確認
        hex =  color_labels[j]
        # hex 轉成rgb
        rgb_ = hex_to_rgb(hex)
        # print('顏色的RGB為:',rgb_)
        # print('顏色的HEX為:',hex)
        #percens
        percents = percentage(label_counts[data],sum(label_counts.values()))
        # print('百分比為:%.1f' %(percents ))
        if  percents >= 0.2:
            colorDict[hex] = percents
        # print('百分比為:%.1f' %(percentage(label_counts[i],sum(label_counts.values()))) )
        j+=1
    return colorDict

def GetColorHex(path):
    maxColor = dict()
    dic = plot_image_info(path)
    x = {k: v for k, v in sorted(dic.items(), key=lambda item: item[1])}
    for i in range(-3,0):
        maxColor.update({list(x.keys())[i]: dic[list(x.keys())[i]]})
    return maxColor
# #test
# path = './train_all/morden/SRHA000015.jpg'
# x = GetColorHex(path)
# print(x)
#存取方式
# print(list(x.keys())[-1]) #最大占比的顏色
# print(list(x.keys())[-2]) #第二大占比的顏色
# print(list(x.keys())[-3]) #第三大占比的顏色
