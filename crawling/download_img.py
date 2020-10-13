#coding=utf-8
import os
import json
import urllib.request
import re
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None) #顯示所有columns
pd.set_option('display.max_rows', None) #顯示所有rows

df = pd.DataFrame() #宣告dataframe

fnamelist = []
def doInDir(somedir):
    fileList = os.listdir(somedir)
    # print(fileList)
    for f in fileList:
        fullpath = os.path.join(somedir, f)
        if os.path.isdir(fullpath):
            doInDir(fullpath) #遞迴走訪
        elif os.path.isfile(fullpath):
            fname = somedir + '/' + f
            a = re.match('^.*.json.*$',fname)
            if a != None:
                print(a)
                fnamelist.append(fname)
            # print(fname)
    return fnamelist

dir_all = doInDir('./CHCCFolders/')

file_dict = dict()

for file in dir_all:
    file_dict.clear()
    print('當前檔案:', file, '處理中...')
    #取得物件類型
    parent_folder = file.split('/')[1]
    object_type = file.split('/')[2]
    filename = file.split('/')[3].split('.')[0]
    # print(filename)

    with open(file,'r',encoding='utf-8') as f:
        file_dict = json.load(f)
        #下載圖片
        save_location = './' + parent_folder + '/' + object_type + '/' + filename + '.jpg' #圖片儲存路徑
        save_layout   = './' + parent_folder + '/' + 'Layout_images' + '/' #儲存layout路徑
        link = urllib.parse.quote(file_dict['Product'], safe=':/')
        # print(link)
        urllib.request.urlretrieve(link, save_location) #下載圖片到資料夾
        cnt = 0
        #讀取layout 圖片
        for i in file_dict['Layout']:
            save_layout_ = save_layout + filename + '({})'.format(cnt) + '.jpg'  # 儲存layout路徑
            try:
                link2 = urllib.parse.quote(i,safe=':/')
                print(link2)
                urllib.request.urlretrieve(link2,save_layout_)
                cnt = cnt + 1
            except ValueError: #url 為空時
                continue 
        #處理json欄位
        df = df.append(file_dict,ignore_index=True)

df.to_csv('./output.csv',encoding='utf-8')
print('處理完畢')
print(df)