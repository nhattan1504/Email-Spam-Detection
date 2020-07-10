

from pandas import DataFrame
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

import readfileinput


def processingModel(acc_score_of_sample_data = True):

    df_train = readfileinput.get_df_train()
    df_test = readfileinput.get_df_test()

    if acc_score_of_sample_data: # print some predict values and show accuracy of sample data
        # get vector
        messages_bow = CountVectorizer(analyzer=readfileinput.seperate_msg).fit_transform(df_train['messages'])
        # split train/test data
        X_train, X_test, y_train, y_test = train_test_split(messages_bow, df_train['spam'], test_size=0.25, shuffle = True)
        # run model
        classifier = MultinomialNB()
        classifier.fit(X_train, y_train)

        # print
        print('Sample data has: '+ str(df_train.shape[0]) + ' mails')
        # print the predictions
        print('Predicted value (15 values): ',classifier.predict(X_test)[:15])
        # print Actual Label
        print('Actual value (15 values): ',y_test.values[:15])

        # evaluate the model on the test data set
        from sklearn.metrics import classification_report,confusion_matrix, accuracy_score
        pred = classifier.predict(X_test)
        print(classification_report(y_test ,pred))
        print('Confusion Matrix: \n', confusion_matrix(y_test,pred))
        print()
        print('Accuracy: ', accuracy_score(y_test,pred))
        print()
        print("#################################################")
        print()


    # append data test to data train and run model to predict data test
    df = df_train.append(df_test, ignore_index=True)
    num_of_mail_tests =df_test.shape[0]

    messages_bow = CountVectorizer(analyzer=readfileinput.seperate_msg).fit_transform(df['messages'])
    X_train, X_test, y_train, y_test = train_test_split(messages_bow, df['spam'], test_size = num_of_mail_tests, shuffle = False)
    classifier = MultinomialNB()
    classifier.fit(X_train, y_train)
    # #Print the predictions
    print('#####  Predict input data  #####')
    print('Input data has: '+ str(num_of_mail_tests) + ' mails')
    print('Predicted value: ',classifier.predict(X_test))
    #Print Actual Label
    print('Actual value: ',y_test.values)
