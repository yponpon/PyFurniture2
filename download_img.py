#下載ikea_json
#coding=utf-8
import os
import json
import urllib.request
import re
import pandas as pd
import numpy as np
import time
import shutil #檔案異動
from urllib.error import HTTPError

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
                fnamelist.append(fname)
            # print(fname)
    return fnamelist

dir_all = doInDir('./IKEAFolders/')
parent_folder = './IKEAImgs'
destination_folder = './Done_json'
file_dict = dict()

for file in dir_all:
    file_dict.clear()
    print('當前檔案:', file, '處理中...')
    #建立下載檔案名稱
    object_type = file.split('/')[2]
    filename = file.split('/')[3].split('.json')[0] #只取檔案名稱
    print(parent_folder)
    print(object_type)
    print(filename)
    #建立移動檔案名稱
    object_type_dest = file.split('/')[2]
    filename_dest = file.split('/')[3]
    dest_full_dir = destination_folder + '/' + object_type_dest + '/' + filename_dest
    print(object_type_dest)
    print(filename_dest)
    print(dest_full_dir)
    cnt = 0
    with open(file,'r',encoding='utf-8') as f:
        file_dict = json.load(f)
        # link = urllib.parse.quote(file_dict['images'], safe=':/')
        # print(link)
        for i in file_dict['images']:
            # 下載圖片
            save_location =  parent_folder + '/' + object_type + '/' + filename + '({})'.format(
                cnt) + '.jpg'  # 圖片儲存路徑
            cnt = cnt + 1
            #print(i)
            try:
                urllib.request.urlretrieve(i, save_location) #下載圖片到資料夾
            except HTTPError: #下載到死圖時跳過
                continue
        #處理json欄位
        df = df.append(file_dict,ignore_index=True)
    #處理完的Json移動到Complete資料夾
    shutil.move(file,dest_full_dir)
df.to_csv('./IKEAFolders/outputikea.csv',encoding='utf-8')
print('處理完畢')
print(df)