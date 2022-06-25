import csv
import pandas as pd
from train import Train
from sklearn.linear_model import LinearRegression
import pickle
import os
import json
from extractfeatures import ExtractFeatues 

class UrlModel:


    def __init__(self):
        print('Hello from urlmodel')
        self.model_file_name = 'finalized_model.sav'
        self.main()


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
        trainset = pd.read_csv ('../urlmodel/datasets/basic.csv')
        trainset = trainset.set_index('id')
        X = trainset.iloc[: , :-1]
        Y = trainset.iloc[: , -1]
        model = LinearRegression()
        print('to shape')
        print(trainset.shape)
        model.fit(X, Y)
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