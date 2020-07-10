# write all keywords (from each mail) to file
import glob
import mailbox
import os
import sys

import preprocessing

# get body of a message (message: 'mboxMessage' type)


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


# write data to file
def writeProcessingFile(updateTrainData=False):
    listOfSpamFiles = glob.glob("data\\preprocessingSpamMails\\*.txt")
    listOfHamFiles = glob.glob("data\\preprocessingHamMails\\*.txt")
    listFileTest = glob.glob("data\\test\\*")

    if listFileTest == []:
        print("Don't have test file !")
        return

    # Write preprocessing input data (test) to folder 'output'
    for i in glob.glob("data\\output\\*"):
        os.remove(i)
    i = 0
    inputMails_fileNames = glob.glob("data\\test\\*")
    for fileName in inputMails_fileNames:
        if fileName[-3:] == 'txt': # file txt which is decoded
            f_read = open(fileName, "r", encoding="UTF-8")
            f_write = open("data/output/" + "outputText" + str(i) + ".txt", "w", encoding="UTF-8")
            f_write.writelines(item + " " for item in preprocessing.text_preprocess(f_read.read()))
            f_write.close()
            i += 1
            continue
        for item in mailbox.mbox(fileName):
            bodyItem = getbody(item)
            if isinstance(bodyItem, str):              
                f = open("data/output/" + "outputText" + str(i) + ".txt", "w", encoding="UTF-8")
                f.writelines(item + " " for item in preprocessing.text_preprocess(bodyItem))
                f.close()
                i += 1


    isFilesExist = listOfSpamFiles != [] and listOfHamFiles != []
    if (not updateTrainData) and isFilesExist:  # File not requiring to update and files have exist
        print("Ok, no update training data")
        return

    if updateTrainData:  # Remove all files before updating
        for i in listOfSpamFiles:
            os.remove(i)
        for i in listOfHamFiles:
            os.remove(i)

    print("Waiting for updating...")

    # Write preprocessing spam data to folder 'inputRawSpamMails'
    i = 0
    spamMails_fileNames = glob.glob("data\\inputRawSpamMails\\*")
    for fileName in spamMails_fileNames:
        for item in mailbox.mbox(fileName):
            bodyItem = getbody(item)
            if isinstance(bodyItem, str):
                f = open("data/preprocessingSpamMails/" + "spam" + str(i) + ".txt", "w", encoding="UTF-8")
                f.writelines(item + " " for item in preprocessing.text_preprocess(bodyItem))
                f.close()
               
                i += 1

    # Write preprocessing ham data to folder 'inputRawSpamMails'
    i = 0
    hamMails_fileNames = glob.glob("data\\inputRawHamMails\\*")
    for fileName in hamMails_fileNames:
        for item in mailbox.mbox(fileName):
            bodyItem = getbody(item)
            if isinstance(bodyItem, str):
                f = open("data/preprocessingHamMails/" + "ham" + str(i) + ".txt", "w", encoding="UTF-8")
                f.writelines(item + " " for item in preprocessing.text_preprocess(bodyItem))
                f.close()
                i += 1
    
    print("Updating is done!")




# writeProcessingFile(False)