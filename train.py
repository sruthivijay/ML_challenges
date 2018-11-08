# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 15:49:38 2018

@author: sruthi.vs
"""
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from sklearn.externals import joblib
from sklearn.utils import shuffle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


train_data = scipy.io.loadmat('train_32x32.mat')


X = train_data['X']
y = train_data['y']

img_index = 10
plt.imshow(X[:,:,:,img_index])
print(y[img_index])

X = X.reshape(X.shape[0]*X.shape[1]*X.shape[2],X.shape[3]).T
y = y.reshape(y.shape[0],)
X, y = shuffle(X, y, random_state=42)
clf = RandomForestClassifier()

print(clf)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf.fit(X_train, y_train)

preds = clf.predict(X_test)

print("Accuracy:", accuracy_score(y_test,preds))

joblib.dump(clf, 'model.pkl')
