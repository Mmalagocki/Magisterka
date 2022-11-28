import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn.metrics as sm
import os; os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

from extractfeatures import ExtractFeatues
from sklearn.model_selection import RandomizedSearchCV
from keras.models import Sequential
from keras.layers import Dense, InputLayer
from keras.wrappers.scikit_learn import KerasRegressor
from keras.optimizers import SGD
from keras.metrics import BinaryAccuracy
from scipy.stats import reciprocal
from pathlib import Path
from keras.models import load_model





class UrlModel:


    def __init__(self):
        self.model_file_name = 'finalized_model.sav'


    def main(self, dataset=None):
        self.normalize_dataset(dataset)
        self.Bestparams()


    def normalize_dataset(self, dataset=None):
        if dataset is None:
            dataset = pd.read_csv ('../urlmodel/datasets/basic.csv')
        dataset = dataset.set_index('id')
        dataset = dataset.replace(0, 0.5)
        dataset = dataset.replace(-1, 0)
        filepath = Path('../urlmodel/datasets/modified.csv')  
        filepath.parent.mkdir(parents=True, exist_ok=True)  
        dataset.to_csv(filepath)


    def load_mymodel(self):
        loaded_model = load_model('model.h5')
        return loaded_model


    def get_accuracy(self):
        dataset = pd.read_csv ('../urlmodel/datasets/modified.csv')
        dataset = dataset.set_index('id')
        trainset = dataset.sample(frac=0.9, random_state=700)
        test = dataset.drop(trainset.index)
        X_test = test.iloc[: , :-1]
        Y_test = test.iloc[: , -1]
        model = self.load_mymodel()
        y_pred = model.predict(X_test)
        print("Mean absolute error =", round(sm.mean_absolute_error(Y_test, y_pred), 2)) 
        print("Mean squared error =", round(sm.mean_squared_error(Y_test, y_pred), 2)) 
        print("Median absolute error =", round(sm.median_absolute_error(Y_test, y_pred), 2)) 
        print("Explain variance score =", round(sm.explained_variance_score(Y_test, y_pred), 2)) 
        print("R2 score =", round(sm.r2_score(Y_test, y_pred), 2))

    def Bestparams(self):
        dataset = pd.read_csv ('../urlmodel/datasets/modified.csv')
        dataset = dataset.set_index('id')
        trainset = dataset.sample(frac=0.9, random_state=700)
        X_train_full = trainset.iloc[: , :-1]
        Y_train_full = trainset.iloc[: , -1]
        X_valid, X_train = X_train_full[:1000], X_train_full[1000:]
        Y_valid, Y_train = Y_train_full[:1000], Y_train_full[1000:]

        params_distribs = {
            "n_hidden": [0, 1, 2, 3, 4, 5, 6],
            "n_neurons": np.arange(1,100),
            "learning_rate": reciprocal(3e-4, 3e-2),
        }
        keras_model = KerasRegressor(self.adjusting_model)
        keras_model.fit(X_train_full, Y_train_full, epochs=100)
        rnd_search_cv = RandomizedSearchCV(keras_model, params_distribs, n_iter=10, cv=3)
        rnd_search_cv.fit(X_train, Y_train, epochs=100,
                        validation_data = (X_valid, Y_valid)
        )

        print(rnd_search_cv.best_params_)
        print(rnd_search_cv.best_score_)


    def train(self, n_neurons=None, learning_rate=None, optimizer=None, input_shape=30):
        dataset = pd.read_csv ('../urlmodel/datasets/modified.csv')
        dataset = dataset.set_index('id')
        trainset = dataset.sample(frac=0.9, random_state=700)
        X_train_full = trainset.iloc[: , :-1]
        Y_train_full = trainset.iloc[: , -1]

        model = self.create_model()
        model.fit(X_train_full, Y_train_full, epochs=100)
        model.save('model.h5')

    def create_model(self, n_neurons=55, learning_rate=0.02902325189497062, optimizer=None, input_shape=30):
        model = Sequential()
        model.add(InputLayer(input_shape = 30))
        model.add(Dense(n_neurons, activation = "relu"))
        model.add(Dense(n_neurons, activation = "relu"))
        model.add(Dense(n_neurons, activation = "relu"))
        model.add(Dense(n_neurons, activation = "relu"))
        model.add(Dense(n_neurons, activation="sigmoid"))
        model.add(Dense(1))
        if optimizer is None:
            optimizer = SGD(learning_rate = learning_rate)
        model.compile(loss="mse", optimizer = optimizer, metrics=BinaryAccuracy())

        return model

    def preprocess_data(self,df):
        df.drop_duplicates(subset=['examined_page'], inplace=True)

        df = df[df.examined_page.str.contains('http')]

        return df

    def adjusting_model(self, n_hidden = 4, n_neurons = 55, learning_rate = 0.02902325189497062, input_shape = 30):
        model = Sequential()
        model.add(InputLayer(input_shape = input_shape))
        
        for layer in range(n_hidden):
            model.add(Dense(n_neurons, activation = "relu"))
        model.add(Dense(n_neurons, activation="sigmoid"))
        model.add(Dense(1))
        optimizer = SGD(learning_rate = learning_rate)
        model.compile(loss="mse", optimizer = optimizer, metrics=BinaryAccuracy())
        return model


    def verify(self, data_to_test):
        if self.model == 0:
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
        results = self.model.predict(extracted_features)
        print(results)