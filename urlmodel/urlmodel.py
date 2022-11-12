import csv
import json
import os
import pickle
from hashlib import new

import numpy as np
import pandas as pd
from extractfeatures import ExtractFeatues
from sklearn import linear_model
from sklearn.metrics import (accuracy_score, mean_absolute_error,
                             mean_squared_error, r2_score)
from train import Train

from sklearn import decomposition, datasets
from sklearn import linear_model
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler


class UrlModel:


    def __init__(self):
        self.model_file_name = 'finalized_model.sav'


    def main(self):
        model = self.read_pickle()

    def read_pickle(self):
        if os.path.isfile(self.model_file_name):
            with open(self.model_file_name, "rb") as f:
                try:
                    return pickle.load(f)
                except Exception: # so many things could go wrong, can't be more specific.
                    pass 
        return 0


    def train(self):
        dataset = pd.read_csv ('../urlmodel/datasets/basic.csv')
        dataset = dataset.set_index('id')
        trainset = dataset.sample(frac=0.9, random_state=700)
        pca = decomposition.PCA()
        stc_slc = StandardScaler()

        test = dataset.drop(trainset.index)
        X_train = trainset.iloc[: , :-1]
        Y_train = trainset.iloc[: , -1]
        X_test = test.iloc[: , :-1]
        Y_test = test.iloc[: , -1]
        elasticnet = linear_model.ElasticNet()
        pipe = Pipeline(steps=[('stc_slc', stc_slc),
                           ('pca', pca),
                           ('elasticnet', elasticnet)])
        n_components = list(range(1,X_train.shape[1]+1,1))

        normalize = [True, False]
        selection = ['cyclic', 'random']
        parameters = dict(pca__n_components=n_components,
                      elasticnet__normalize=normalize,
                      elasticnet__selection=selection)

        clf_EN = GridSearchCV(pipe, parameters)
        clf_EN.fit(X_train, Y_train)
        print('Best Number Of Components:', clf_EN.best_estimator_.get_params()['pca__n_components'])
        print(clf_EN.best_estimator_.get_params()['elasticnet'])
        exit()
        # pred_y = model.predict(X_test)
        # y_test = Y_test.to_numpy()
        print(model.score(X_test, Y_test))
        # print(model.coef_)

        filename = 'finalized_model.sav'
        pickle.dump(model, open(filename, 'wb'))


    def preprocess_data(self,df):
        df.drop_duplicates(subset=['examined_page'], inplace=True)

        df = df[df.examined_page.str.contains('http')]

        return df

    def verify(self, data_to_test):
        model = self.read_pickle()
        if model == 0:
            self.train()
        data_to_test = self.preprocess_data(data_to_test)

        extracted_features = []
        i = 0
        for row in data_to_test['examined_page']:
            i += 1
            print('Link {}/{} is being processed'.format(i, len(data_to_test)))
            extracted = ExtractFeatues()
            extracted_features.append(extracted.checkFeatures(row))
            if i > 9:
                break
        results = model.predict(extracted_features)
        print(results)