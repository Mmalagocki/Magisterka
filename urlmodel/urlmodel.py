import csv
import pandas as pd
from train import Train
from sklearn import linear_model
import pickle
import os
import json
from extractfeatures import ExtractFeatues 
from sklearn.metrics import mean_absolute_error,r2_score,mean_squared_error
import numpy as np

class UrlModel:


    def __init__(self):
        print('Hello from urlmodel')
        self.model_file_name = 'finalized_model.sav'


    def main(self):
        model = self.read_pickle()
        if model == 0:
            trainset = pd.read_csv ('../urlmodel/datasets/basic.csv')
            trainset = trainset.set_index('id')
            X = trainset.iloc[: , :-1]
            Y = trainset.iloc[: , -1]
            model = LinearRegression()
            model.fit(X, Y)
            # print(model.score(X, Y))
            # print(model.coef_)
            filename = 'finalized_model.sav'
            pickle.dump(model, open(filename, 'wb'))


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
        trainset = dataset.sample(frac=0.8, random_state=700)
        test = dataset.drop(trainset.index)
        X = trainset.iloc[: , :-1]
        Y = trainset.iloc[: , -1]
        Test_X = test.iloc[: , :-1]
        true_Y = test.iloc[: , -1]
        # print(len(true_Y))
        # print(len(Test_X))
        # exit()
        model = linear_model.Lasso(alpha=0.6)
        # print('to shape')
        # print(trainset.shape)
        model.fit(X, Y)
        pred_y = model.predict(Test_X)
        print("R^2 : ", r2_score(true_Y, pred_y))
        print("MAE :", mean_absolute_error(true_Y,pred_y))
        print("RMSE:",np.sqrt(mean_squared_error(true_Y, pred_y)))
        exit()
        # print(model.score(X, Y))
        # print(model.coef_)

        filename = 'finalized_model.sav'
        pickle.dump(model, open(filename, 'wb'))


    def preprocess_data(self,df):
        df.drop_duplicates(subset=['Link_without_base_url'], inplace=True)
        return df


    def test(self, data_to_test):
        model = self.read_pickle()
        if model == 0:
            self.train()
        data_to_test = self.preprocess_data(data_to_test)

        extracted_features = []
        i = 0
        for row in data_to_test['Link_without_base_url']:
            i += 1
            print('Link {}/{} is being processed'.format(i, len(data_to_test)))
            extracted = ExtractFeatues()
            extracted_features.append(extracted.checkFeatures(row))
        results = model.predict(extracted_features)
        print(results)