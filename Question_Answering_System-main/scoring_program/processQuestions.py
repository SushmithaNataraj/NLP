import nltk

allQuestionType = {"why", "whose", "what", "where", "when", "how", "who"}

'''
    question: question string
    Return: type of question. The type could be anyhting in ["why", "whose", "what", "where", "when", "how", "who"]
    This function assumes that each question would have only one WH word and it returns after finding the first occurence of a WH word
'''


def findQuestionType(question):
    wordsInQuestion = nltk.word_tokenize(question)
    for word in wordsInQuestion:
        if word in allQuestionType:
            return word
    return ''
