import random

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

        self.CROSS_VALIDATION_EPOCHS = 250
        self.CROSS_VALIDATION_LEARNING_RATE = 0.1

        self.training()


    def training(self):
        self.folding()

        for fold in self.trainsetfolded:
            training_set = self.trainsetfolded.copy()
            training_set.remove(fold)
            training_set = sum(training_set, [])
            validation_set = list(fold.copy())

            fold_error, weights = self.train(training_set, validation_set, self.CROSS_VALIDATION_LEARNING_RATE, self.CROSS_VALIDATION_EPOCHS)
            error += fold_error

        self.train()


    def calculate(self, row, coef):
        y = coef[0]

        for i in range(len(row) - 1):
            y += coef[i + 1] * row[i]

        return y


    def get_weights(self, inputs, expected, weights, learning_rate):
        for i in range(len(inputs)):
            row = inputs[i]
            y = expected[i]

            prediction = self.calculate(row, weights)
            error = prediction - y
            weights[0] = weights[0] - learning_rate * error * 1

            for i in range(len(row) - 1):
                weights[i + 1] = weights[i + 1] - learning_rate * error * row[i]

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

        weights = [random.uniform(-1, 1) for i in range(len(training_set[0]) + 1)]

        error_counter = 0
        last_validate_error = None
        best_validate_error = 0
        best_weights = weights

        for epoch in range(CROSS_VALIDATION_EPOCHS):
            weights = self.get_weights(train_target, train_target_output, weights, CROSS_VALIDATION_LEARNING_RATE)
        print(weights)
        exit()

