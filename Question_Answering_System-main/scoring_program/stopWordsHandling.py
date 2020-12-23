import nltk
from nltk.corpus import stopwords

stopWords = set(stopwords.words('english'))

'''
    sentence: a string whose stop words need to be removed
    Return: a string without stop words
    This function simply checks if the current word in belongs to stop words set. If not it adds it to te output list.
'''

def removeStopWords(sentence):
    wordsInSentence = nltk.word_tokenize(sentence)
    sentenceWithoutStopWords = " ".join([word for word in wordsInSentence if word not in stopWords])
    return sentenceWithoutStopWords
