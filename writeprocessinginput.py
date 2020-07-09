import glob
import mailbox
import preprocessing
import os
import sys


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


def writeProcessingInput(update=False):
    listOfFiles = glob.glob("data\\preprocessingSpamMails\\*.txt")
    isFilesExist = listOfFiles != []

    if (not update) and isFilesExist:
        print("hihi")
        return

    if update:
        for i in listOfFiles:
            os.remove(i)
    

    listMails = list()
    i = 0
    spamMails_fileNames = glob.glob("data/inputRawSpamMails/*.mbox")
    for fileName in spamMails_fileNames:
        for item in mailbox.mbox(fileName):
            bodyItem = getbody(item)
            if isinstance(bodyItem, str):
                f = open("data/preprocessingSpamMails/" + str(i) + ".txt", "w", encoding="UTF-8")
                f.writelines(item + " "  for item in preprocessing.text_preprocess(bodyItem))

                # listMails.append(preprocessing.text_preprocess(bodyItem)
                f.close()
                i += 1


# writeProcessingInput(True)



