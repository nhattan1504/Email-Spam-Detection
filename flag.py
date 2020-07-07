import mailbox
import sys 
import base64
import re
from pyvi import ViTokenizer 
import pandas as pd 
import urllib
from gensim import utils
from gensim.parsing.porter import PorterStemmer
from gensim.parsing.preprocessing import strip_tags, strip_non_alphanum, strip_multiple_whitespaces,preprocess_string, split_alphanum, strip_short, strip_numeric
import nltk
from nltk.corpus import stopwords
from pandas import DataFrame
import numpy as np


# Get stopwords Vi & Eng
def getStopwordsVN(arrayOfFileName):
    stopwords_VN = list()
    for fileName in arrayOfFileName:
        f = open(fileName, "r", encoding="utf-8")
        for each_word in f:
            stopwords_VN.append(f.readline().split('\n')[0])
    return stopwords_VN
def getStopwordsVN_ENG():
    stopwordsVN_fileNames = [] # file names
    stopwordsVN_fileNames.append("vietnamese-stopwords.txt")
    stopwordsVN_fileNames.append("vietnamese-stopwords-dash.txt")

    stopwordsVN = getStopwordsVN(stopwordsVN_fileNames)
    stopwordsENG = stopwords.words('english')
    return stopwordsVN + stopwordsENG 


# Normalize body items (string)
RE_NUMERIC_DEL = re.compile(r"[0-9]*[a-zA-Z]*[0-9]+[a-zA-Z]*[0-9]*", re.UNICODE)
def strip_number_alphabets(s): # delete a word which has numbers and alphabets. Ex: abc1, 2z3
    s = utils.to_unicode(s)
    return RE_NUMERIC_DEL.sub("", s)
def text_preprocess(bodyItem): # bodyItem: string
    # Remove http, https
    bodyItem = re.sub(r'^https?:\/\/.*[\r\n]*', '', bodyItem, flags=re.MULTILINE)
    bodyItem = re.sub(r'^http?:\/\/.*[\r\n]*', '', bodyItem, flags=re.MULTILINE)
    bodyItem = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ", bodyItem)
    # Decode some bodyItems which are not decoded
    bodyItem = bodyItem.replace("=", "%")
    bodyItem = urllib.parse.unquote(bodyItem)
    # Remove a word which has numbers and alphabets
    bodyItem = strip_number_alphabets(bodyItem)
    # Remove meaningless words, convert to lower words and split meaningful words 
    bodyItem = strip_non_alphanum(bodyItem).lower().strip()
    bodyItem = split_alphanum(bodyItem)
    # Join two words which have meaning in Vietnamese. Ex: hội thảo -> hội_thảo
    bodyItem = ViTokenizer.tokenize(bodyItem)
    # Remove a word which has one letter
    bodyItem = strip_short(bodyItem, minsize=2)
    # Remove stopwords
    words = [word for word in bodyItem.split() if word not in getStopwordsVN_ENG()]
    return words


# get body of a message
def getbody(message): 
    body = None
    if message.is_multipart():
        for part in message.walk():
            if part.is_multipart():
                for subpart in part.walk():
                    if subpart.get_content_type() == 'text/plain':
                        body = subpart.get_payload(decode=False)
            elif part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=False)
    elif message.get_content_type() == 'text/plain':
        body = message.get_payload(decode=False)
    return body


listMails = list()
i = 0
for item in mailbox.mbox('Spam - DTT.mbox'):
    if i < 100:
        bodyItem = getbody(item)
        if isinstance(bodyItem, str):
            # print(str(i) + "~~~~~~~~~~BEGIN~~~~~~~~~~~~~~~~~~~~")
            # print(text_preprocess(bodyItem))
            # print("~~~~~~~~~~~END~~~~~~~~~~~~~~~~~~~")
            #text_preprocess(bodyItem)
            listMails.append(text_preprocess(bodyItem))
    i += 1


print(len(listMails))
df = DataFrame({'messages':0, 'spam':0})
for mail in listMails:
    listToStr = ''
    listToStr = ' '.join(map(str, mail)) 
    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    # print(listToStr)

    d = {'messages': listToStr, 'spam': np.ones(len(mail)) }
    df1 = DataFrame(d)
    df.append(df1, ignore_index = True) 
    

print(df["messages"])