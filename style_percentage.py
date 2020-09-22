from keras.models import load_model
from keras.preprocessing import image
from keras import backend as K
import numpy as np
import os
import cv2
import json
#dimesions of images
img_width,img_height = 299,299
os.environ['CUDA_VISIBLE_DEVICES'] = '-1' #使用CPU運算
class inception_retrain(object):
    def __init__(self):
        self.img=None
        self.model=None
        self.InV3model=None
    def _load_image(self,img):
        '''Takes an image
            Returns its proper form to feed into model's predcition '''
        #image = cv2.imread('test/{}'.format(img))
        fd = open(img,'rb')
        img_str = fd.read()
        fd.close()
        nparr = np.fromstring(img_str, np.uint8)
        image = cv2.imdecode(nparr, -1)[:,:,:3] #imdecode flag = -1 Unchanged
        image = cv2.resize(image, (299, 299))
        image = np.expand_dims(image/255, axis=0)
        image = np.vstack([image])
        return image
    def _feature_extraction_inception(self,img):
        image=self._load_image(img)
        self.img=image
        features=self.InV3model.predict(image)
        return features
    def _load_model(self):
        if self.model is None:
            self.model=load_model('./Models/inV3_last_layer_final_ver.h5')
        if self.InV3model is None:
            self.InV3model=load_model("./Models/inception.h5")
    def predict(self,img):
        '''Takes an imagebbb
           Return the predicted probabilities for each class'''
        self._load_model()
        image=self._feature_extraction_inception(img)
        self.img=image
        pred=self.model.predict(image)
        # pred=np.round(pred,3).reshape(4,)
        pred=np.round(pred,3).reshape(3,)
        # return pred[0],pred[1],pred[2],pred[3]
        return pred[0],pred[1],pred[2]

def model_check(path):
    label = ['Morden','northEur','Rustic']
    Predlist = list()
    model = inception_retrain()
    pred1,pred2,pred3 = model.predict(path)
    Predlist.append(pred1)
    Predlist.append(pred2)
    Predlist.append(pred3)
    K.clear_session() #清空記憶體
    # print(Predlist) #測試用
    return label[Predlist.index(max(Predlist))] #取得a最大的index

# model_check(path='./train_all/morden/SRHA000015.jpg')