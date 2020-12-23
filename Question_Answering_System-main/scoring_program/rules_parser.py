import string

from constants import *
import parser as p


def word_match(question, morph_story_sentence_words):
    """ 
    Refer page number 2(bottom left para)
    Verb matches are weighed more heavily than non verb matches. Can you change it accordingly?
    """
    verbs_more_weightage = []
    question_pos_words = p.pos_tagger(question)
    for word, pos_tag in question_pos_words.items():
        if pos_tag == "VERB":
            verbs_more_weightage.append(word)
    verbs_more_weightage = p.morphological_roots(verbs_more_weightage)

    question_no_stop_words_punct = p.removeStopWords(question)
    question_no_stop_words_punct = question_no_stop_words_punct.translate(str.maketrans('', '', string.punctuation))
    morphological_root_of_question = p.word_tokenizer(question_no_stop_words_punct)
    morphological_root_of_question = p.morphological_roots(morphological_root_of_question)

    score = 0
    for morph_story_word in morph_story_sentence_words:
        if morph_story_word in morphological_root_of_question:
            if morph_story_word in verbs_more_weightage:
                score = score + 6
            else:
                score = score + 3
        elif morph_story_word in verbs_more_weightage:
            score = score + 6
    return score


def find_where_rules_score(question, story_sentence, morphed_sentence):
    """
    Summary Line:
    Where questions almost always look for a specific location.
    Finds the over all score for this sentnce by applying various rules defined below

    Parameters:
    question(string): A question with stop words (original question)
    story_sentence(string): A sentence inside the story

    Return:
    int: Overall integer scrore for this sentence
    """
    score = 0
    # Rule 1: general word matching function
    score += word_match(question, morphed_sentence)

    tokenized_words = p.word_tokenizer(story_sentence)
    
    # Rule 2: identifies location preposition
    for word in tokenized_words:
        if word in location_preposition:
            score += good_clue

    # Rule 3: looks for sentences with words belonging to LOCATION semantic class
    named_entities = p.entity_recognizer(story_sentence)
    # print("The named entities", named_entities)
    for entity, label in named_entities.items():
        if label in spacy_location_labels or entity in LOCATION:
            score += confident
            # Need to add one more check here to identify LOCATION
            if entity in LOCATION:
                score += good_clue
            # Rule that I added
            if "locate" in question.lower():
                score += 2*slam_dunk 
    return score


def is_name_in_sentence_frag(sentence_frag):
    sentence_noun_phrase_chunk = p.get_noun_chunks_list(sentence_frag)

    sentence_contain_name = False
    for noun_phrase in sentence_noun_phrase_chunk:
        if p.is_name(noun_phrase):
            sentence_contain_name = True
            return sentence_contain_name
    return sentence_contain_name


def is_human_in_sentence(sentence_frag):
    tokenized_words = p.word_tokenizer(sentence_frag)
    for word in tokenized_words:
        if p.is_human(word):
            return True
    return False


def find_who_rules_scores(question, story_sentence, morphed_sentence):
    """
    Rules defined for 'who' type of questions
    :param question: A question with stop words (original question)
    :param story_sentence: A single sentence of a story
    :return: Score of this sentence after applying
    """
    score = 0
    # Rule 1
    score += word_match(question, morphed_sentence)

    # Rule 2
    '''print(type(question))
    print(type(morphed_sentence))
    print(type(' '.join(morphed_sentence)))
    print(' '.join(morphed_sentence))
    print(type(story_sentence))'''
    story_sentence_morphed = ' '.join(morphed_sentence)
    if not is_name_in_sentence_frag(question):
        if is_name_in_sentence_frag(story_sentence_morphed):
            score += confident

    # Rule #3
    if not is_name_in_sentence_frag(question):
        if "name" in story_sentence_morphed:
            score += good_clue

    # Rule #4
    if is_name_in_sentence_frag(story_sentence_morphed) or is_human_in_sentence(story_sentence_morphed):
        score += good_clue

    return score


def find_best_sentence_for_why_rules(question, morph_story_sentence_dict):
    """
    Summary Line:
    All the sentences are assigned a score using the word_match function. Then the sentences with the top score are isolated. These are the BEST sentences. 
    Every sentence is then applied a score 0 and WHY rules are applied. 
    ########### IMP: CURRENTLY I AM ASSUMING THAT THERE IS ONLY ONE BEST SENTENCE ###########

    Parameters:
    question(string): Original Question
    morph_story_sentence_dict(dict): {sentence_number :[original_sentence, [morphed sentence words]]}

    Returns:
    score(int): the score of the sentence that best matches answer to the why question. 

    """
    
    for sentence_number, sentence_list in morph_story_sentence_dict.items():
        score = 0
        original_sentence, morphed_sentence_words = sentence_list[0], sentence_list[1]
        score = word_match(question, morphed_sentence_words)
        morph_story_sentence_dict[sentence_number] = [original_sentence, morphed_sentence_words, score]
    ordered_items = sorted(morph_story_sentence_dict.items(), key = lambda x:x[1][2], reverse=True)
    # print(ordered_items)
    best_sentence_index = ordered_items[0][0]
    best_sentence = ordered_items[0][1][0]
    best_sentence_score = ordered_items[0][1][2]
    # print("*********** The best sentence ******************** ")
    # print(best_sentence)
    return morph_story_sentence_dict, best_sentence_index, best_sentence, best_sentence_score

    
        

def find_why_rules_score(story_sentence, cur_sentence_index, best_sentence_index, best_sentence_score, cur_sentence_score):
    """
    Summary Line:
    WHY questions are handled differently than other questions.
    The WHY rules are based on the observation that the answer to WHY question often appears immediately
    before/after the sentence that most closely matches the question. This is due to the
    causal nature of WHY questions.
    The caller of this function should call WORDMATCH on all the sentences and decide the BEST sentence.
    After finding the BEST sentence, reinitialize the score of the other sentences to 0.
    (ASSUMING THAT THE BEST SENTENCE SCORE SHOULD BE INTIALIZED TO ZERO AS WELL.)
    
    Parameters:
    story_sentence(string): A string containing a sentence in the story
    cur_sentence_index: Index of the 'story_sentence' inside te story
    best_sentence_index: Index of the 'BEST sentence' inside the story
    best_sentence_score: Score of the sentence that best matched wordmatch()
    cur_senetnce_score: Score of the current sentence against wordmatch()

    Returns:
    int: Overall integer score for this sentence
    """
    
    score = 0
    tokenized_words = p.word_tokenizer(story_sentence)
    # Rule 1: Rewards all the sentences that produced the BEST word match score
    if cur_sentence_score == best_sentence_score:
        score += clue

    # Rule 2: If S immed. preceeds member of BEST
    if cur_sentence_index == best_sentence_index - 1:
        score += clue

    # Rule 3: If S immed. follows member of BEST
    elif cur_sentence_index == best_sentence_index + 1:
        score += good_clue

    # Rule 4: Reawrds sentences that contain the word 'want'
    if "want" in story_sentence:
        score += good_clue
    
    # Rule 5: Rewards the sentences that contain the word 'so' or 'because'
    for word in tokenized_words:
        if word.lower() == "so" or word.lower() == "because":
            # if cur_sentence_score == best_sentence_score:
            #     score += confident
            score += good_clue
        # Rules I added
        elif word.lower() in {"if", "after"}:
            if cur_sentence_score == best_sentence_score:
                score += good_clue
            
    return score


def find_when_rules_score(question, story_sentence, morphed_sentence):
    story_sentence = story_sentence.replace('\n', ' ').strip()

    score = 0
    word_match_score = word_match(question, morphed_sentence)
    sent_tokenized_words = p.word_tokenizer(story_sentence)
    question_tokenized_words = p.word_tokenizer(question)

    # Rule #1: Sentence contain any time expression
    named_entities = p.entity_recognizer(story_sentence)

    for entity, label in named_entities.items():
        if label in date_time_labels:
            score += good_clue
            score += word_match_score

    # Rule #2
    for sent_word in sent_tokenized_words:
        if "the last" in question and sent_word.lower() in {"first", "last", "since", "ago"}:
            score += slam_dunk

    # Rule #3:
    question_contain_start_begin = False
    for question_word in question_tokenized_words:
        if question_word.lower() in {"start", "begin"}:
            question_contain_start_begin = True
            break

    if question_contain_start_begin:
        for sent_word in sent_tokenized_words:
            if sent_word.lower() in {"start", "begin", "since", "year"}:
                score += slam_dunk

    return score


def find_what_rules_score(question, story_sentence, morphed_sentence):
    """
    Summary Line:
    WHAT rules seek an amazing variety of answers

    """
    score = 0
    # Rule 1: Generic wordMatch function
    score += word_match(question, morphed_sentence)

    # Rule 2: Rewards sentences that contain date expression if the question contains a month of the year
    question_tokens = p.word_tokenizer(question)
    days = {"today", "yesterday", "tomorrow", "last night"}

    question_has_month = set(question_tokens).intersection(MONTH)
    for day in days:
        if day in story_sentence.lower() and question_has_month:
            score += clue

    # Rule 3: Several 'what kind?' questions look for a description of an object
    # Rule 3 rewards sentences that contain the word call or from.(It is called .., it is made from..)
    if "kind" in question.lower():
        if "call" in story_sentence.lower() or "from" in story_sentence.lower():
            score += good_clue

    # Rule 4: Looks for words associated with names in both question and sentence
    if "name" in question.lower():
        if "name" in story_sentence.lower() or "call" in story_sentence.lower() or "known" in story_sentence.lower():
            score += slam_dunk

    # Rule 5: Very specific and recognizes questions that conatain phrases such as 'name of <x>' or
    # 'name for <x>'. Any sentence that contains a proper noun whose head noun matches x will be highly rewarded.
    #  Ex 'What is the name of creek?' ans: "Pigeon Creek"
    #

    return score


# def find_how_rules_score(question, sentence, morphed_sentence):
#     score = 0

#     # Rule 1: Generic wordMatch function
#     score += word_match(question, morphed_sentence)
    
#     named_entities = p.entity_recognizer(sentence)
#     tokenized_words = p.word_tokenizer(sentence)
#     #Rule 2: Rewards the sentences that contain numbers if question conatains 'quantifiers'
#     for entity, label in named_entities.items():
#         if label in {"QUANTITY", "MONEY", "PERCENT", "DATE"}:
#             score += good_clue

#     question_tokens = p.word_tokenizer(question)
#     for word in question_tokens:
#         if word in quantifiers:
#             for sent_word in tokenized_words or sent_word in quantifiers:
#                 if sent_word.isdigit():
#                     score += confident
#     return score

def find_how_rules_score(question, sentence, morphed_sentence):
    score = 0

    # Rule 1: Generic wordMatch function
    score += word_match(question, morphed_sentence)
    
    named_entities = p.entity_recognizer(sentence)
    tokenized_words = p.word_tokenizer(sentence)
    
    # If question contains big, small etc, reward the sentences, that contain quantity
    quantity = ["big", "small", "tall"]
    money = ["cost", "much", "expensive"]
    adjectives = ["old", "age", "long", "often", "year", "month"]
    # if question contains any of the above quantities, and answer contains quantifiers, reward them
    if any(quant in question.lower() for quant in quantity):
        for entity, label in named_entities.items():
            if label in "QUANTITY":
                score += confident

    
    elif any(m in question.lower() for m in money):
        for entity, label in named_entities.items():
            if label in "MONEY":
                score += confident

    
    elif any(adj in question.lower() for adj in adjectives):
        if any(adj in sentence.lower() for adj in sentence):
            score += confident
    #Rule 2: Rewards the sentences that contain numbers if question conatains 'quantifiers'
    # for entity, label in named_entities.items():
    #     if label in set(["QUANTITY", "MONEY", "PERCENT", "DATE"]):
    #         score += good_clue

    question_tokens = p.word_tokenizer(question)
    for word in question_tokens:
        if word in quantifiers:
            for sent_word in tokenized_words or sent_word in quantifiers:
                if sent_word.isdigit():
                    score += good_clue
    return score
