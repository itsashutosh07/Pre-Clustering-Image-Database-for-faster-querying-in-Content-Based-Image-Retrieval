import pickle
import numpy as np
from numpy import linalg as LA
from keras.utils import load_img, img_to_array
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input

class VGGNet:
    def __init__(self):
        # weights: 'imagenet'
        # pooling: 'max' or 'avg'
        # input_shape: (width, height, 3), width and height should >= 48
        self.input_shape = (224, 224, 3)
        self.weight = 'imagenet'
        self.pooling = 'max'
        self.model = VGG16(weights = self.weight, input_shape = (self.input_shape[0], self.input_shape[1], self.input_shape[2]), pooling = self.pooling, include_top = False)
        self.model.predict(np.zeros((1, 224, 224 , 3)))

    '''
    Use vgg16 model to extract features
    Output normalized feature vector
    '''
    def extract_feat(self, img_path):
        img = load_img(img_path, target_size=(self.input_shape[0], self.input_shape[1]))
        img = img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input(img)
        feat = self.model.predict(img, verbose = False)
        norm_feat = feat[0]/LA.norm(feat[0])
        return norm_feat

# def ChangePath(input_path):
# 	our_path=input_path
# 	our_path=our_path[2:len(our_path)]
# 	our_path="\\reviews\\media\\"+our_path 
# 	#print(our_path)
# 	return our_path

def normal_method(path, k):
    k = int(k)
    
    model = VGGNet()
    file = open("reviews\cluster_dict", "rb")
    cluster_dict = pickle.load(file)
    file.close()
    
    queryVec = model.extract_feat(path)
    scores = {}
    for key in cluster_dict:
        for img in cluster_dict[key]["images"]:
            scores[img[1]] = np.dot(queryVec, img[0])

    sorted_scores = sorted(scores, key = scores.get, reverse=True)
    res = []
    for p in sorted_scores:
        if k > 0:
            res.append((p, scores[p]))
            k -= 1
        else:
            break
    
    return res

def improved_method(path, k):
    k = int(k)
    model = VGGNet()
    file = open("reviews\cluster_dict", "rb")
    cluster_dict = pickle.load(file)
    file.close()
    
    
    queryVec = model.extract_feat(path)
    scores  = {}
    for key in cluster_dict:
        scores[key] = np.dot(queryVec, cluster_dict[key]["center"])
    
    top_cluster = max(scores, key = scores.get)
    scores = {}
    
    for img in cluster_dict[top_cluster]["images"]:
        scores[img[1]] = np.dot(queryVec, img[0])
    
    sorted_scores = sorted(scores, key = scores.get, reverse=True)
    res = []

    for p in sorted_scores:
        if k > 0:
            # this -- "./database\\Leopards\\image_0184.jpg"
            # to  -- "reviews\media\database\Leopards\\image_0184.jpg"
            l=p.decode().split("\\");
            relPath="";
            for i in l:
                relPath=relPath+"\\"+i
            relPath=relPath[3:len(relPath)]
            relPath="reviews\\media\\"+relPath 
            print(relPath)
            res.append((relPath, round(scores[p], 3)))
            k -= 1
        else:
            break
    
    return res

# res = normal_method("./queries/1.jpg", 5)
# print(res)
# print()

# res = improved_method("./queries/1.jpg", 5)
# print(res)
# print()