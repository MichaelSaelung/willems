import cv2 as cv
from os import walk, path
import pickle
import constan
from constan import region
import numpy as np
from sklearn.model_selection import train_test_split
#import matplotlib.pyplot as plt
#from random import shuffle

def createDataSet(region = region.CANINE, IMAGE_SIZE = constan.IMAGE_SIZE , ASCII_A = constan.ASCII_A):
    dataset = []
    for (dirPath, _,fileNames) in walk(constan.DATASET_FOLDER +region):
        for fileName in fileNames:
            if fileName.endswith(constan.IMAGE_TYPE):
                try:
                    object_array = cv.imread(path.join(dirPath, fileName),-1)
                    object_array = cv.resize(object_array, (IMAGE_SIZE,IMAGE_SIZE))
                    class_array = ord(dirPath.split('/')[-1]) - ASCII_A
                    dataset.append([object_array, class_array])
                except :pass
    #shuffle(dataset)
    pickle_out = open(f'{constan.PICKLE_FOLDER}{region}.pickle','wb')
    pickle.dump(dataset, pickle_out)
    pickle_out.close()        
    #plt.imshow(dataset[0][0])
    #plt.show()

    return dataset

def loadDataSet(region = region.CANINE):
    features = []
    labels = []
    try:
        for feature, label in pickle.load(open(f'{constan.PICKLE_FOLDER}{region}.pickle','rb')):
            features.append(feature)
            labels.append(label)
        labels = np.array(labels)
        features = np.array(features) / 255.0
        X_train, X_test, y_train, y_test  = train_test_split(features, labels, test_size=0.3,random_state=42)
        #print(labels.shape)
        #print(features.shape)
    except:pass
    
    return X_train, X_test, y_train, y_test  

def createNewImage(imgPath, IMAGE_SIZE = constan.IMAGE_SIZE):
    object_array = cv.imread(imgPath)
    object_array = cv.resize(object_array, (IMAGE_SIZE,IMAGE_SIZE))

    object_array = np.array(object_array).reshape(-1,IMAGE_SIZE,IMAGE_SIZE,3)
    newImg = object_array/255.0

    return newImg