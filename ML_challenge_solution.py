# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import re
import datetime
from nltk.corpus import stopwords
from sklearn.preprocessing import LabelEncoder
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
import xgboost as xgb

pd.set_option('display.max_colwidth',100)
In [177]:
#load data
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')
In [98]:
# convert unix time format
unix_cols = ['deadline','state_changed_at','launched_at','created_at']

for x in unix_cols:
    train[x] = train[x].apply(lambda k: datetime.datetime.fromtimestamp(int(k)).strftime('%Y-%m-%d %H:%M:%S'))
    test[x] = test[x].apply(lambda k: datetime.datetime.fromtimestamp(int(k)).strftime('%Y-%m-%d %H:%M:%S'))
Some features
In [99]:
cols_to_use = ['name','desc']
len_feats = ['name_len','desc_len']
count_feats = ['name_count','desc_count']

for i in np.arange(2):
    train[len_feats[i]] = train[cols_to_use[i]].apply(str).apply(len)
    test[len_feats[i]] = test[cols_to_use[i]].apply(str).apply(len)
In [100]:
train['name_count'] = train['name'].str.split().str.len()
train['desc_count'] = train['desc'].str.split().str.len()

test['name_count'] = test['name'].str.split().str.len()
test['desc_count'] = test['desc'].str.split().str.len()
In [101]:
train['keywords_len'] = train['keywords'].str.len()
train['keywords_count'] = train['keywords'].str.split('-').str.len()

test['keywords_len'] = test['keywords'].str.len()
test['keywords_count'] = test['keywords'].str.split('-').str.len()
Some more features
In [102]:
# converting string variables to datetime
unix_cols = ['deadline','state_changed_at','launched_at','created_at']

for x in unix_cols:
    train[x] = train[x].apply(lambda k: datetime.datetime.strptime(k, '%Y-%m-%d %H:%M:%S'))
    test[x] = test[x].apply(lambda k: datetime.datetime.strptime(k, '%Y-%m-%d %H:%M:%S'))
In [103]:
# there should be simpler way - might take longer
# creating list with time difference between 1) launched_at and created_at 2) deadline and launched_at

time1 = []
time3 = []
for i in np.arange(train.shape[0]):
    time1.append(np.round((train.loc[i, 'launched_at'] - train.loc[i, 'created_at']).total_seconds()).astype(int))
    time3.append(np.round((train.loc[i, 'deadline'] - train.loc[i, 'launched_at']).total_seconds()).astype(int))
In [104]:
train['time1'] = np.log(time1)
train['time3'] = np.log(time3)
In [105]:
# for test data
time5 = []
time6 = []
for i in np.arange(test.shape[0]):
    time5.append(np.round((test.loc[i, 'launched_at'] - test.loc[i, 'created_at']).total_seconds()).astype(int))
    time6.append(np.round((test.loc[i, 'deadline'] - test.loc[i, 'launched_at']).total_seconds()).astype(int))
In [106]:
test['time1'] = np.log(time5)
test['time3'] = np.log(time6)
In [107]:
feat = ['disable_communication','country']

for x in feat:
    le = LabelEncoder()
    le.fit(list(train[x].values) + list(test[x].values))
    train[x] = le.transform(list(train[x]))
    test[x] = le.transform(list(test[x]))
In [109]:
train['goal'] = np.log1p(train['goal'])
test['goal'] = np.log1p(test['goal'])
Text Cleaning
In [110]:
# creating a full list of descriptions from train and etst
kickdesc = pd.Series(train['desc'].tolist() + test['desc'].tolist()).astype(str)
In [111]:
# this function cleans punctuations, digits and irregular tabs. Then converts the sentences to lower
def desc_clean(word):
    p1 = re.sub(pattern='(\W+)|(\d+)|(\s+)',repl=' ',string=word)
    p1 = p1.lower()
    return p1

kickdesc = kickdesc.map(desc_clean)
In [113]:
stop = set(stopwords.words('english'))
kickdesc = [[x for x in x.split() if x not in stop] for x in kickdesc]

stemmer = SnowballStemmer(language='english')
kickdesc = [[stemmer.stem(x) for x in x] for x in kickdesc]

kickdesc = [[x for x in x if len(x) > 2] for x in kickdesc]

kickdesc = [' '.join(x) for x in kickdesc]
Creating Count Features
In [147]:
# Due to memory error, limited the number of features to 650
cv = CountVectorizer(max_features=650)
In [148]:
alldesc = cv.fit_transform(kickdesc).todense()
In [150]:
#create a data frame
combine = pd.DataFrame(alldesc)
combine.rename(columns= lambda x: 'variable_'+ str(x), inplace=True)
In [157]:
#split the text features

train_text = combine[:train.shape[0]]
test_text = combine[train.shape[0]:]

test_text.reset_index(drop=True,inplace=True)
Finalizing train and test data before merging
In [162]:
cols_to_use = ['name_len','desc_len','keywords_len','name_count','desc_count','keywords_count','time1','time3','goal']
In [198]:
target = train['final_status']
In [168]:
train = train.loc[:,cols_to_use]
test = test.loc[:,cols_to_use]
In [174]:
X_train = pd.concat([train, train_text],axis=1)
X_test = pd.concat([test, test_text],axis=1)
In [175]:
print X_train.shape
print X_test.shape
(108129, 659)
(63465, 659)
Model Training
In [180]:
dtrain = xgb.DMatrix(data=X_train, label = target)
dtest = xgb.DMatrix(data=X_test)
In [185]:
params = {
    'objective':'binary:logistic',
    'eval_metric':'error',
    'eta':0.025,
    'max_depth':6,
    'subsample':0.7,
    'colsample_bytree':0.7,
    'min_child_weight':5
    
}
In [186]:
# You can probably get better accuracy with rounds > 1000. 
bst = xgb.cv(params, dtrain, num_boost_round=1000, early_stopping_rounds=40,nfold=5L,verbose_eval=10)
bst_train = xgb.train(params, dtrain, num_boost_round=1000)
In [188]:
p_test = bst_train.predict(dtest)
In [189]:
sub = pd.DataFrame()
sub['project_id'] = test['project_id']
sub['final_status'] = p_test
In [194]:
sub['final_status'] = [1 if x > 0.5 else 0 for x in sub['final_status']]
In [196]:
sub.to_csv("xgb_with_python_feats.csv",index=False) #0.70