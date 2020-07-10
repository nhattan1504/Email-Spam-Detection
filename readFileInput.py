# read files which has preprocessed and convert these files to dataframe
from pandas import DataFrame
import pandas as pd 
import glob

import writeprocessingfile


def seperate_msg(msg):
    return [word for word in msg.split()]

# return a dataframe of list of spam mails
def get_df_spam(): 
    df_spam = DataFrame()
    listFileInputs = glob.glob("data/preprocessingSpamMails/*.txt")
    for fileInputName in listFileInputs:
        f = open(fileInputName, "r", encoding="UTF-8")
        msg = ''
        msg = f.read()
        d = {'messages':[msg], 'spam': ["1"] }
        df_temp = DataFrame(d)
        df_spam = df_spam.append(df_temp, ignore_index = True) 
        f.close()
    df_spam.drop_duplicates(inplace = True)
    df_spam['messages'].head().apply(seperate_msg)
    return df_spam


# return a dataframe of list of ham mails
def get_df_ham(): 
    df_ham = DataFrame()
    listFileInputs = glob.glob("data/preprocessingHamMails/*.txt")
    for fileInputName in listFileInputs:
        f = open(fileInputName, "r", encoding="UTF-8")
        msg = ''
        msg = f.read()
        d = {'messages':[msg], 'spam': ["0"] }
        df_temp = DataFrame(d)
        df_ham = df_ham.append(df_temp, ignore_index = True) 
        f.close()
    df_ham.drop_duplicates(inplace = True)
    df_ham['messages'].head().apply(seperate_msg)
    return df_ham


# return a dataframe which combines list of ham and spam mails
def get_df_train():
    df_train = DataFrame()
    df_spam = get_df_spam()
    df_ham = get_df_ham()
    df_train = df_spam.append(df_ham, ignore_index = True)
    return df_train


# return a dataframe of test data
def get_df_test():
    df_test = DataFrame()
    listFileInputs = glob.glob("data/output/*.txt")
    for fileInputName in listFileInputs:
        f = open(fileInputName, "r", encoding="UTF-8")
        msg = ''
        msg = f.read()
        d = {'messages':[msg], 'spam': ["-1"] } # -1: undefined, unassigned label
        df_temp = DataFrame(d)
        df_test = df_test.append(df_temp, ignore_index = True) 
        f.close()
    df_test.drop_duplicates(inplace = True)
    df_test['messages'].head().apply(seperate_msg)
    return df_test


