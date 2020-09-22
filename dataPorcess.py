#####################################################################################
#取得風格、顏色、配置轉為onehot陣列
#####################################################################################
import pandas
import get_color #取得顏色
import ColorToName #取得顏色對應欄位
import style_percentage #取得圖片風格
import cv2
from os import walk
import json
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1' #使用CPU運算
######################################################################################
# imgPath = 圖片路徑
imgPath = './train_all/morden'

#fileDict: Jons Dict, 將當前的圖片資料轉為Json欄位
fileDIct = dict()

#Json Save: Json檔案儲存路徑
Json_Save = './Json_save'
######################################################################################

#讀取圖片
def getStyle(path):
    #取得該圖片風格
    style = style_percentage.model_check(path)
    return style
def load_images_from_folder(folder):
    filelist = []
    for (dirpath,dirnames,filenames) in walk(folder):
        filelist.extend(filenames)
        break
    return filelist


#整理資料
imglist = load_images_from_folder(imgPath)
for file in imglist:
    fileDIct.clear()
    print('當前檔案:',file,'處理中...')
    filePath = imgPath + '/' + file
    fileDIct[file] = {'file':file}
    #取得風格
    style = getStyle(filePath)
    fileDIct[file]['Style'] = style
    #取得顏色
    color = get_color.GetColorHex(filePath)
    NewColor_dic = ColorToName.get_dictionary(color)
    #顏色跟占比加入json檔中
    for k,v in NewColor_dic.items():
        fileDIct[file][k] = v
    print(fileDIct)

    save_name = './Json_save/' + file + '.json'
    with open(save_name,'w') as f:
        json.dump(fileDIct,f)