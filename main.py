import argparse
from multiprocessing import freeze_support
import gensim
from gensim.models import LdaModel
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
import nltk
import pandas as pd
from sklearn.datasets import fetch_20newsgroups
from gensim.test.utils import datapath
import os.path

'''
Write a function to perform the pre processing steps on the entire dataset
'''

stemmer = SnowballStemmer("english")
def lemmatize_stemming(text):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))


# Tokenize and lemmatize
def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))

    return result

if __name__ == '__main__':
    freeze_support()
    if os.path.isfile('lda.model') == False:
        newsgroups_train = fetch_20newsgroups(subset='train', shuffle = True)
        # newsgroups_test = fetch_20newsgroups(subset='test', shuffle = True)


        stemmer = SnowballStemmer("english")
        original_words = ['caresses', 'flies', 'dies', 'mules', 'denied','died', 'agreed', 'owned',
                   'humbled', 'sized','meeting', 'stating', 'siezing', 'itemization','sensational',
                   'traditional', 'reference', 'colonizer','plotted']
        singles = [stemmer.stem(plural) for plural in original_words]

        pd.DataFrame(data={'original word':original_words, 'stemmed':singles })


        '''
        Preview a document after preprocessing
        '''
        document_num = 50
        doc_sample = 'This disk has failed many times. I would like to get it replaced.'

        # print("Original document: ")
        words = []
        for word in doc_sample.split(' '):
            words.append(word)
        # print(words)
        # print("\n\nTokenized and lemmatized document: ")
        # print(preprocess(doc_sample))

        processed_docs = []

        i = 0
        for doc in newsgroups_train.data:
            i+=1
            # print(i)
            processed_docs.append(preprocess(doc))

        '''
        Preview 'processed_docs'
        # '''
        # print(processed_docs[:2])
        '''
        Create a dictionary from 'processed_docs' containing the number of times a word appears 
        in the training set using gensim.corpora.Dictionary and call it 'dictionary'
        '''
        dictionary = gensim.corpora.Dictionary(processed_docs)

        '''
        Checking dictionary created
        '''
        count = 0
        for k, v in dictionary.iteritems():
            print(k, v)
            count += 1
            if count > 10:
                break

        '''
        OPTIONAL STEP
        Remove very rare and very common words:
        
        - words appearing less than 15 times
        - words appearing in more than 10% of all documents
        '''
        # dictionary.filter_extremes(no_below=15, no_above=0.1, keep_n= 100000)

        '''
        Create the Bag-of-words model for each document i.e for each document we create a dictionary reporting how many
        words and how many times those words appear. Save this to 'bow_corpus'
        '''
        bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

        '''
        Preview BOW for our sample preprocessed document
        '''
        document_num = 20
        bow_doc_x = bow_corpus[document_num]

        for i in range(len(bow_doc_x)):
            print("Word {} (\"{}\") appears {} time.".format(bow_doc_x[i][0],
                                                             dictionary[bow_doc_x[i][0]],
                                                             bow_doc_x[i][1]))


        # LDA mono-core -- fallback code in case LdaMulticore throws an error on your machine
        # lda_model = gensim.models.LdaModel(bow_corpus,
        #                                    num_topics = 10,
        #                                    id2word = dictionary,
        #                                    passes = 50)

        # LDA multicore
        '''
        Train your lda model using gensim.models.LdaMulticore and save it to 'lda_model'
        '''
        # TODO
        lda_model = gensim.models.LdaMulticore(bow_corpus,
                                           num_topics = 8,
                                           id2word = dictionary,
                                           passes = 10,
                                           workers = 2)

        # for idx, topic in lda_model.print_topics(-1):
        #     # print("Topic: {} \nWords: {}".format(idx, topic ))
        #     # print("\n")

        # temp_file = datapath("lda.model")
        lda_model.save('lda.model')

    # num = 100
    # unseen_document = newsgroups_test.data[num]
    lda_model = LdaModel.load('lda.model')

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--training_data_file")
    args = vars(parser.parse_args())
    training_data_file = args['training_data_file']

    file = open(training_data_file, "r")

    processed_docs = []
    newsgroups_train = fetch_20newsgroups(subset='train', shuffle = True)
    i = 0
    for doc in newsgroups_train.data:
        i+=1
        # print(i)
        processed_docs.append(preprocess(doc))

    my_document = file.read()
    dictionary = gensim.corpora.Dictionary(processed_docs)

    '''
    Checking dictionary created
    '''
    count = 0
    for k, v in dictionary.iteritems():
        # print(k, v)
        count += 1
        if count > 10:
            break

    '''
    OPTIONAL STEP
    Remove very rare and very common words:

    - words appearing less than 15 times
    - words appearing in more than 10% of all documents
    '''
    # dictionary.filter_extremes(no_below=15, no_above=0.1, keep_n=100000)
    # Data preprocessing step for the unseen document
    # print(my_document)
    bow_vector = dictionary.doc2bow(preprocess(my_document))
    Best_score = {"Score": 0, "Topic": ""}
    for index, score in sorted(lda_model[bow_vector], key=lambda tup: -1*tup[1]):
        Score, Topic = score, lda_model.print_topic(index, 1)
        if Best_score["Score"] < float(Score):
            Best_score["Score"] = float(Score)
            Best_score["Topic"] = Topic
        # print("Score:" + str(Score) +" Topic:" + str(Topic))
        #
        # print("Score: {}\t Topic: {}".format(score, lda_model.print_topic(index, 1)))
    print(Best_score)
    # print(newsgroups_test.target[num])


