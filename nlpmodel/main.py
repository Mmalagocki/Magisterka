import csv
import pandas as pd

def main():
    trainset = pd.read_csv ('./datasets/basic.csv')
    columns = trainset.shape[1]



if __name__ == '__main__':
    main()