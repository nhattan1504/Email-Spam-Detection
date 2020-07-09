from pandas import DataFrame
import pandas as pd 
import glob

import writeprocessinginput



# print(len(listMails))

# df = DataFrame({'messages':[0], 'spam':[0]})
df = DataFrame()
listFileInputs = glob.glob("data/preprocessingSpamMails/*.txt")
for fileInputName in listFileInputs:
    f = open(fileInputName, "r", encoding="UTF-8")
    msg = ''
    msg = f.read()

    d = {'messages':[msg], 'spam': ["1"] }
    df1 = DataFrame(d)
    df = df.append(df1, ignore_index = True) 
    f.close()

print(df.head())
df.drop_duplicates(inplace = True)
print(df.shape)
print(df.isnull().sum())
