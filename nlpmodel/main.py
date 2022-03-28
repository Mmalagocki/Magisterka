import csv
import pandas as pd

def main():
    trainset = pd.read_csv ('./datasets/basic.csv')
    print(trainset)
    exit()
    columns = trainset.shape[1]
    print(trainset)
    print(columns)


if __name__ == '__main__':
    main()