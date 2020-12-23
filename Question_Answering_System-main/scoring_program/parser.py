import nltk
import spacy
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
#from nltk.stem import WordNetLemmatizer
import constants

nlp = spacy.load("en_core_web_sm")

stopWords = set(stopwords.words('english'))


def morphological_roots(list_of_words):
    """
    Summary line:
    Function that finds the morphological roots of a list of words

    Parameters:
    sentence(string): a string whose stop words need to be removed

    Returns:
    set: a set of words with their morphological roots

    """
    porter_stemmer = PorterStemmer()
    #wordnet_lemmatizer = WordNetLemmatizer()
    for word_index in range(0, len(list_of_words)):
        list_of_words[word_index] = porter_stemmer.stem(list_of_words[word_index])
        #list_of_words[word_index] = wordnet_lemmatizer.lemmatize(list_of_words[word_index])
    return list_of_words


def removeStopWords(sentence):
    """
    Summary line:
    This function simply checks if the current word belongs to stop words set. If not it adds it to te output list.

    Parameters:
    sentence(string): a string whose stop words need to be removed

    Returns:
    string: a string without stop words

    """

    wordsInSentence = nltk.word_tokenize(sentence)
    sentenceWithoutStopWords = " ".join([word for word in wordsInSentence if word not in stopWords])
    return sentenceWithoutStopWords


def word_tokenizer(sentence):
    """
    Summary Line:
    Converts the given sentence into list of words, punctuations

    Parameters:
    sentence(string): Sentence needs to be tokenized

    Returns:
    list: A list of words, punctuations in the sentence
    """

    return nltk.word_tokenize(sentence)


def pos_tagger(sentence):
    """
    Summary Line:
    Finds the POS for each word in the sentence

    Parametrs:
    sentence(string): A sentence

    Returns:
    dict: key being the word and value being the POS tag for the word
    """

    doc = nlp(sentence)
    pos_dict = {}
    for token in doc:
        pos_dict[token.text] = token.pos_
    return pos_dict


def entity_recognizer(sentence):
    """
    Summary Line:
    Finds the named entities in the sentence

    Parameters:
    sentence(string): A sentence

    Returns:
    dict: key being the entity and value being the label for that entity
    """

    doc = nlp(sentence)
    entity_dict = {}
    for ent in doc.ents:
        entity_dict[ent.text] = ent.label_
    return entity_dict


def get_noun_chunks_list(sentence):
    """
    Function returns a list of noun phrase
    :param sentence: a string for which noun phrases need to be found out
    :return: list of noun phrases for the given sentence
    """
    doc = nlp(sentence)
    noun_chunks_list = list(doc.noun_chunks)
    return noun_chunks_list


def is_proper_noun(noun_phrase):
    noun_phrase_words = word_tokenizer(str(noun_phrase))
    for word in noun_phrase_words:
        if not word[0].isupper():
            return False
    return True


def is_human(word):
    """
    :param word: word to find if it is part of HUMAN set
    :return: true if word is part of HUMAN set else false
    """
    if word.lower() in constants.human_class:
    # if word in constants.human_class:
        return True
    return False


def is_name(noun_phrase):
    is_name_bool = False
    if is_proper_noun(noun_phrase):
        noun_phrase_words = word_tokenizer(str(noun_phrase))
        for word in noun_phrase_words:
            if is_human(word):
                is_name_bool = True
        return is_name_bool
    else:
        return False


def answer_cleanup(sentence, question):
    #sentence = removeStopWords(sentence)
    #sentence = sentence.translate(str.maketrans('', '', string.punctuation))

    question_morph = morphological_roots(word_tokenizer(question))
    # question_entities = p.entity_recognizer(question)
    sentence_morph = morphological_roots(word_tokenizer(sentence))
    sentence_words = word_tokenizer(sentence)

    for question_word in question_morph:
        if question_word in sentence_morph:
            index = sentence_morph.index(question_word)
            sentence_morph.pop(index)
            sentence_words.pop(index)
    sentence = ' '.join(sentence_words)

    return sentence
