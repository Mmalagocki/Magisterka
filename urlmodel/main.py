import csv
import pandas as pd
from train import Train

def main():
    trainset = pd.read_csv ('./datasets/basic.csv')
    columns = trainset.shape[1]
    trainset = trainset.set_index('id')
    Train(trainset, columns)


if __name__ == '__main__':
    main()