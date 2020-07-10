# Filer keywords from body mail
import re
from pyvi import ViTokenizer 
import urllib
from gensim import utils
from gensim.parsing.porter import PorterStemmer
from gensim.parsing.preprocessing import strip_tags, strip_non_alphanum, strip_multiple_whitespaces,preprocess_string, split_alphanum, strip_short, strip_numeric
import glob

import stopwordsVN_ENG


# Normalize body items (string)
RE_NUMERIC_DEL = re.compile(r"[0-9]*[a-zA-Z]*[0-9]+[a-zA-Z]*[0-9]*", re.UNICODE)
def strip_number_alphabets(s): # delete a word which has numbers and alphabets. Ex: abc1, 2z3
    s = utils.to_unicode(s)
    return RE_NUMERIC_DEL.sub("", s)
def text_preprocess(bodyItem): # bodyItem: string (of one mail)  => return: list of words (of one mail)
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
    words = [word for word in bodyItem.split() if word not in stopwordsVN_ENG.getStopwordsVN_ENG()]
    return words
