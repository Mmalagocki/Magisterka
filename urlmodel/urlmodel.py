import csv
import json
import os
import pickle
from hashlib import new
from tensorflow.keras import models, layers, utils, backend as K
import matplotlib.pyplot as plt
import shap

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


    # define metrics
    def Recall(self, y_true, y_pred):
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())
        return recall

    def Precision(self, y_true, y_pred):
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision

    def F1(self, y_true, y_pred):
        precision = self.Precision(y_true, y_pred)
        recall = self.Recall(y_true, y_pred)
        return 2*((precision*recall)/(precision+recall+K.epsilon()))

    def train(self):
        dataset = pd.read_csv ('../urlmodel/datasets/basic.csv')
        dataset = dataset.set_index('id')
        trainset = dataset.sample(frac=0.9, random_state=700)
        model = self.create_model(trainset.shape[1])
        # model.summary()
        model.compile(optimizer='adam', loss='binary_crossentropy', 
              metrics=['accuracy',self.F1])
        test = dataset.drop(trainset.index)
        X_train = trainset.iloc[: , :-1]
        Y_train = trainset.iloc[: , -1]
        X_test = test.iloc[: , :-1]
        Y_test = test.iloc[: , -1]
        training = model.fit(x=X_train, y=Y_train, batch_size=32, epochs=100, shuffle=True, verbose=2, validation_split=0.3)
        print("finished")
        # plot
        metrics = [k for k in training.history.keys() if ("loss" not in k) and ("val" not in k)]    
        fig, ax = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(15,3))
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
                        units=int(round((n_features+1)/2)), 
                        activation='relu'),
            layers.Dropout(name="drop1", rate=0.2),
            
            ### hidden layer 2
            layers.Dense(name="h1", units=int(round((n_features+1)/4)), 
                        activation='relu'),
            layers.Dropout(name="drop2", rate=0.2),
            
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