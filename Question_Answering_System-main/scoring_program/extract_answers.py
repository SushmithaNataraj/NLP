import string
import rules_parser
import parser as p
import constants


def find_story_sentence_scores(morph_story_sentences_dict, question_type, question):
    # call the rule function
    if question_type == "why":
        morph_story_sentences_dict, best_sentence_index, best_sentence, best_sentence_score = rules_parser.find_best_sentence_for_why_rules(question, morph_story_sentences_dict)
   
    for sent_number, sentence_list in morph_story_sentences_dict.items():
        score = 0
        original_sentence, morphed_sentence_list = sentence_list[0], sentence_list[1]
        if question_type == "who":
            score = rules_parser.find_who_rules_scores(question, sentence_list[0], sentence_list[1]) # 0 - original, 1 - morphed
        elif question_type == "where":
            score = rules_parser.find_where_rules_score(question, sentence_list[0], sentence_list[1])
        elif question_type == "why":
            cur_score = morph_story_sentences_dict[sent_number][2]
            score = rules_parser.find_why_rules_score(original_sentence, sent_number, best_sentence_index, best_sentence_score, cur_score)
        elif question_type == "what":
            score = rules_parser.find_what_rules_score(question, original_sentence, morphed_sentence_list)
        elif question_type == "when":
            score = rules_parser.find_when_rules_score(question, sentence_list[0], sentence_list[1])
        elif question_type == "how":
            score = rules_parser.find_how_rules_score(question, original_sentence, morphed_sentence_list)
        elif question_type == "whom":
            score = rules_parser.find_who_rules_scores(question, sentence_list[0], sentence_list[1])
        elif question_type == "whose":
            score = rules_parser.find_who_rules_scores(question, sentence_list[0], sentence_list[1])
        elif question_type == "which":
            pass
        morph_story_sentences_dict[sent_number] = [original_sentence, morphed_sentence_list
                                                   , score]
    answer = find_matching_story_sentence(morph_story_sentences_dict, question_type, question)
    return answer


def extract_where_answer(sentence, question):
    # Where is something located?
    sentence = sentence.replace('\n', ' ')
    answer_sentence = ''
    named_entities = p.entity_recognizer(sentence)
    if len(named_entities) == 1:
        for key in named_entities:
            answer_sentence += key
        return answer_sentence
        
    if "locate" or "live" in question.lower():
        # print("The sentence is:", sentence, "\nThe question is:",question)
        entities = []
        for entity, label in named_entities.items():
            if label == "GPE" or label == "LOC" or label in constants.LOCATION:
                entities.append(entity)
        entity = ' '.join(entities)
        if entity:
            return entity
        else:
            sentence = p.answer_cleanup(sentence, question)
            return sentence
    return p.answer_cleanup(sentence, question)


def extract_why_answer(sentence, question):
    sentence = sentence.replace('\n', ' ')
    answer_sentence = ''
    if "because" in sentence.lower():
        words = sentence.lower().split()
        i = -1
        for i, word in enumerate(words):
            if "because" in word:
                return " ".join(words[i:])
        
    if "so" in sentence.lower():
        words = sentence.lower().split()
        i = -1
        for i, word in enumerate(words):
            if "so" in word:
                return " ".join(words[i:])
    
    if "following" in sentence.lower():
        words = sentence.lower().split()
        i -= 1
        for i, word in enumerate(words):
            if "following" in word:
                return " ".join(words[i:])

    return sentence


def extract_who_answer(sentence, question, matching_sentence_number, morph_story_sentences_dict):
    sentence = sentence.replace('\n', ' ').strip()
    question_token = p.word_tokenizer(question)
    sent_entities = p.entity_recognizer(sentence)
    answer = ""
    for sent_entity, label in sent_entities.items():
        if label == "PERSON":
            if sent_entity not in question:
                answer = str(sent_entity)
                return answer
        elif label == "ORG":
            if sent_entity not in question:
                answer = str(sent_entity)
                return answer
    if not answer:
        sentence_pos = p.pos_tagger(sentence)
        pos_tags = sentence_pos.values()
        if "PRON" in pos_tags:
            answer = ""
            for i in range(matching_sentence_number - 1, -1, -1):
                previous_sentence = morph_story_sentences_dict.get(i)[0]
                previous_sentence = previous_sentence.replace('\n', ' ')
                previous_sentence = previous_sentence.translate(str.maketrans('', '', string.punctuation))
                previous_sentence_words = p.word_tokenizer(previous_sentence)
                for previous_sentence_words_index in range(len(previous_sentence_words) - 1, -1, -1):
                    word_pos_dict = p.entity_recognizer(previous_sentence_words[previous_sentence_words_index])
                    entity_values = list(word_pos_dict.values())
                    if "PERSON" in entity_values:
                        answer = list(word_pos_dict.keys())[0] + " " + answer
                if answer:
                    break
            if answer:
                return answer
            return p.answer_cleanup(sentence, question)
        else:
            return p.answer_cleanup(sentence, question)
    return p.answer_cleanup(sentence, question)


def extract_how_answer(sentence, question):
    tokenized_words = p.word_tokenizer(sentence)
    named_entities = p.entity_recognizer(sentence)
    # If question contains big, small etc, reward the sentences, that contain quantity
    quantity = ["big", "small", "tall"]
    # if question contains any of the above quantities, and answer contains quantifiers, reward them
    if any(quant in question.lower() for quant in quantity):
        for entity, label in named_entities.items():
            if label in "QUANTITY":
                return entity
    money = ["cost", "dollar", "expensive"]
    if any(m in question.lower() for m in money):
        money_entities = []
        for entity, label in named_entities.items():
            if label in "MONEY":
                #return entity
                money_entities.append(entity)
                for money_entity_index in range(len(money_entities)):
                    if money_entities[money_entity_index].isdigit():
                        num_index = tokenized_words.index(money_entities[money_entity_index])
                        if tokenized_words[num_index - 1] in constants.currency_symbols:
                            money_entities[money_entity_index] = tokenized_words[num_index - 1] + money_entities[money_entity_index]
                return ' '.join(money_entities)
    time = ["time", "long", "many"]
    if any(t in question.lower() for t in time):
        for entity, label in named_entities.items():
            if label in "TIME":
                return entity
    return sentence


def extract_when_answer(sentence, question):
    sentence = sentence.replace('\n', ' ')
    answer = ""
    sent_entities = p.entity_recognizer(sentence)
    for sent_entity, label in sent_entities.items():
        if label == "DATE":
            answer = answer + sent_entity + " "
    if answer:
        return answer
    return sentence

def extract_what_answer(sentence, question):
    return p.answer_cleanup(sentence, question)
    # remove all the stop words 
    pass


def find_answer(sentence, question_type, question, matching_sentence_number, morph_story_sentences_dict):
    if question_type == "where":
        return extract_where_answer(sentence, question)
    elif question_type == "who":
        return extract_who_answer(sentence, question, matching_sentence_number, morph_story_sentences_dict)
    elif question_type == "when":
        return extract_when_answer(sentence, question)
    if question_type == "how":
        return extract_how_answer(sentence, question)
    if question_type == "why":
        return extract_why_answer(sentence, question)
    if question_type == "what":
        return extract_what_answer(sentence, question)
    return sentence


def find_matching_story_sentence(morph_story_sentences_dict, question_type, question):
    max_score = 0
    matching_sentence = ''
    matching_sentence_number = -1
    for sentence_number, sentence_elements in morph_story_sentences_dict.items():
        sentence, score = sentence_elements[0], sentence_elements[2]
        if score > max_score:
            max_score = score
            matching_sentence = sentence
            matching_sentence_number = sentence_number
    return find_answer(matching_sentence, question_type, question, matching_sentence_number, morph_story_sentences_dict)


def question_iterator(question_pair_lst, morph_story_sentences_dict, output_file):
    for question_pair in question_pair_lst:
        question = question_pair["Question"]
        question_type = question_pair["Type"]
        answer = find_story_sentence_scores(morph_story_sentences_dict, question_type, question)
        answer = answer.strip('\n')
        answer = answer.replace('\n', ' ')
        question_id_write = "QuestionID: " + question_pair["QuestionID"].strip()
        question = "Question: " + question.strip()
        answer_write = "Answer: " + answer + "\n"
        print(question_id_write)
        # print(question)
        print(answer_write)
        output_file.write(question_id_write)
        output_file.write("\n")
        output_file.write(answer_write)
        output_file.write("\n")
