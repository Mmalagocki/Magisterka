from email import iterators
from pickle import bytes_types
import random
import re

from urllib3 import Retry

class Train:


    def __init__(self, trainset, columns):
        self.trainset = trainset.values.tolist()
        self.trainsetfolded = trainset.values.tolist()
        self.train_target_output = []
        self.train_taget = []
        self.N = columns
        self.K_FOLDS = 11
        self.TRAINING_EPOCHS = 1000
        self.TRAINING_LEARNING_RATE = 0.01
        self.EPSYLON = 0.001

        self.CROSS_VALIDATION_EPOCHS = 250
        self.CROSS_VALIDATION_LEARNING_RATE = 0.1

        self.training()





    def normalize(self, train_target):
        for i in range(len(train_target)):
            N = len(train_target[i])
            for j in range(N):
                train_target[i][j] = train_target[i][j] / N

        return train_target


    def calculate(self, row, coef):
        y = 0
        for i in range(len(row) - 1):
            y += coef[i] * row[i]

        return y


    def get_weights(self, inputs, expected, weights, learning_rate):
        for i in range(len(inputs)):
            row = inputs[i]
            y = expected[i]
            prediction = self.calculate(row, weights)
            # Nie możemy przyjmować 1 i -1 jako rozwiązania
            # Przykładowe rozwiązanie powinno wynosić np 32 i powinno mieć ostateczną etykietę -1
            # Trzeba wprowadzić normalizację z zakresu 0,1. Przy czym rozpatrywać będzięmy wartości -1,1 gdzie im bliżej -1 tym strona bardziej legitna a im bliżej 1 tym mniej
            error = prediction - y
            weights[0] = weights[0] - learning_rate * error * 1

            for j in range(len(row)):
                weights[j] = weights[j] - learning_rate * error * row[j]

        return weights



    def folding(self):
        folds = []
        fold_size = int(len(self.trainsetfolded) / self.K_FOLDS)
        train_data_copy = list(self.trainsetfolded.copy())
        for i in range(self.K_FOLDS):
            fold = []
            while len(fold) < fold_size:
                index = random.randrange(len(train_data_copy))
                fold.append(train_data_copy.pop(index))
            folds.append(fold)
        
        self.trainsetfolded = folds


    def validate(self, inputs, expected, coef):
        summation = 0

        for i in range(len(inputs)):
            row = inputs[i]
            exp = expected[i]
            prediction = self.calculate(row, coef)
            summation = summation + pow(exp - prediction, 2)

        mse = summation / len(inputs)

        return mse


    def training(self):
        self.folding()
        iterations = 0
        best_validate_error = None
        best_weights = None

        for fold in self.trainsetfolded:
            training_set = self.trainsetfolded.copy()
            training_set.remove(fold)
            training_set = sum(training_set, [])
            validation_set = list(fold.copy())

            fold_error, weights = self.train(training_set, validation_set, self.CROSS_VALIDATION_LEARNING_RATE, self.CROSS_VALIDATION_EPOCHS)

            if best_validate_error is None or best_validate_error > fold_error:
                best_validate_error = fold_error
                best_weights = weights
                iterations = 0
            else: 
                iterations += 1

            if iterations > 100:
                return best_weights

        
        return best_weights



    def train(self, training_set, validation_set, CROSS_VALIDATION_LEARNING_RATE, CROSS_VALIDATION_EPOCHS):
        train_target = []
        train_target_output = []
        validate_target = []
        validate_target_output = []
        
        for j in training_set.copy():
            train_target_output.append(j[-1])
            train_target.append(j[:-1])
        for j in validation_set.copy():
            validate_target_output.append(j[-1])
            validate_target.append(j[:-1])
        
        train_target = self.normalize(train_target)

        weights = [random.uniform(-1, 1) for i in range(len(train_target[0]))]

        for epoch in range(CROSS_VALIDATION_EPOCHS):
            print('Epoch %s/%d'% (epoch + 1,CROSS_VALIDATION_EPOCHS))
            weights = self.get_weights(train_target, train_target_output, weights, CROSS_VALIDATION_LEARNING_RATE)

        mse = self.validate(validate_target, validate_target_output, weights)

        return mse, weights

