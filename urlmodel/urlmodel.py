import csv
import json
import os
import pickle
from hashlib import new

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
from extractfeatures import ExtractFeatues
from scipy.stats import randint as sp_randInt
from scipy.stats import uniform
from scipy.stats import uniform as sp_randFloat
from sklearn import datasets, decomposition, linear_model
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import (accuracy_score, make_scorer, mean_absolute_error,
                             mean_squared_error, precision_score, r2_score)
from sklearn.model_selection import (GridSearchCV, RandomizedSearchCV,
                                     cross_val_score, train_test_split)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from tensorflow.keras import backend as K
from tensorflow.keras import layers, models, utils
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from train import Train

import os; os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

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
        X_train = trainset.iloc[: , :-1]
        Y_train = trainset.iloc[: , -1]
        test = dataset.drop(trainset.index)
        X_test = test.iloc[: , :-1]
        Y_test = test.iloc[: , -1]

        model = self.create_model(trainset.shape[1])
        # model.summary()
        model.compile(optimizer='adam', loss='binary_crossentropy', 
              metrics=['accuracy'])

        parameters = {'learning_rate': sp_randFloat(),
                'subsample'    : sp_randFloat(),
                'max_depth'    : sp_randInt(4, 10)
                }
        model.fit(X_train, Y_train, epochs = 150, batch_size = 30, verbose = 2)
        # evaluate the keras model
        accuracy = model.evaluate(X_train, Y_train, verbose=2)
        print(accuracy)
        
        clf = RandomizedSearchCV(estimator = model, param_distributions = parameters, scoring=r2_score, cv = 2, n_iter = 10, n_jobs=-1)

        training = clf.fit(X_train, Y_train, batch_size=32, epochs=100, shuffle=True, verbose=2, validation_split=0.3)
        print(training.best_params_)
        print("finished")
        # plot
        # metrics = [k for k in training.history.keys() if ("loss" not in k) and ("val" not in k)]    
        # fig, ax = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(15,3))
        exit()
        ## training    
        ax[0].set(title="Training")    
        ax11 = ax[0].twinx()    
        ax[0].plot(training.history['loss'], color='black')    
        ax[0].set_xlabel('Epochs')    
        ax[0].set_ylabel('Loss', color='black')    
        for metric in metrics:        
            ax11.plot(training.history[metric], label=metric)   
            ax11.set_ylabel("Score", color='steelblue')    
        ax11.legend()
                
        ## validation    
        ax[1].set(title="Validation")    
        ax22 = ax[1].twinx()    
        ax[1].plot(training.history['val_loss'], color='black')    
        ax[1].set_xlabel('Epochs')    
        ax[1].set_ylabel('Loss', color='black')    
        for metric in metrics:          
            ax22.plot(training.history['val_'+metric], label=metric)    
            ax22.set_ylabel("Score", color="steelblue")    
        plt.show()

        filename = 'finalized_model.sav'
        # pickle.dump(model, open(filename, 'wb'))

    def preprocess_data(self,df):
        df.drop_duplicates(subset=['examined_page'], inplace=True)

        df = df[df.examined_page.str.contains('http')]

        return df

    def create_model(self, n_features):
        model = models.Sequential(name="DeepNN", layers=[
            ### hidden layer 1
            layers.Dense(name="input", input_dim=n_features-1,
                        units=300, 
                        activation='relu'),
            layers.Dropout(name="drop1", rate=0.2),
            
            ### hidden layer 2
            layers.Dense(name="h1",units = 100, 
                        activation='sigmoid'),
            layers.Dropout(name="drop2", rate=0.2),
            
            layers.Dense(name="h2", units=10, 
                        activation='sigmoid'),
            layers.Dropout(name="drop3", rate=0.2),
            
            ### layer output
            layers.Dense(name="output", units=1, activation='sigmoid')
        ])

        return model


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