from parser import word_tokenizer
from constants import all_question_type


def read_questions_file(questions_file):
    """
    Summary Line:
    This function returns a list containing each line in the questions file

    Parameters:
    questions_file(File): File containing all the  question IDs, Questions and Difficulty

    Returns:
    list: A list containing each line of the questions_file
    """

    with open(questions_file) as fp:
        file_content = fp.readlines()
    fp.close()
    return file_content

def find_question_components(question_file_content_lst):
    """
    Summary Line:
    Given a  list containing question file lines as a list, this function groups each question ID, 
    question and difficulty into a dictionary and stores all such dictionaries in a list

    Parameters:
    question_file_content_lst(list): A list containg lines in the question file

    Returns:
    list: [{questionId:..., question:..., Difficulty:...},{questionId:..., question:..., Difficulty:...},{...}, ...]
    """

    question_pairs = []
    question_dict = {}
    for question_component in question_file_content_lst:
        if question_component != "\n":
            question_component_parts = question_component.strip(
                "\n").split(":")
            question_attr, question_attr_values = question_component_parts[0], question_component_parts[1]
            if question_attr == "QuestionID":
                question_dict["QuestionID"] = question_attr_values
            elif question_attr == "Question":
                question_dict["Question"] = question_attr_values
            else:
                question_dict["Difficulty"] = question_attr_values

        else:
            if question_dict:
                question_pairs.append(question_dict)
                question_dict = {}
    if question_dict:
        question_pairs.append(question_dict)

    return question_pairs


def find_question_type(question):
    """
    Summary Line:
    This function assumes that each question would have only one WH word and it returns after finding the first occurence of a WH word

    Parameters:
    question(String): a single question string

    Returns:
    string: type of question. The type could be anyhting in ["why", "whose", "what", "where", "when", "how", "who"]
    """

    wordsInQuestion = word_tokenizer(question)
    
    for word in wordsInQuestion:
        if word.lower() in all_question_type:
            return word.lower()
    return ''

def add_question_type(question_pair_lst):
    """
    Summary Line:
    This function adds an additional key i,e 'Type' to list containing dictionary of question items

    Parameters:
    question_pair_lst(list of dictionaries): [{questionId:..., question:..., Difficulty:...},{...}, ...]

    Returns:
    list of dictionaries: [{questionId:..., question:..., Difficulty:..., Type:...},{questionId:..., question:..., Difficulty:..., Type:...},{...}, ...]
    """

    for index in range(len(question_pair_lst)):
        question_item_dict = question_pair_lst[index]
        question = question_item_dict["Question"]
        type_ = find_question_type(question)
        question_item_dict["Type"] = type_
        question_pair_lst[index] = question_item_dict

    return question_pair_lst


def process_questions_file(questions_file):
    """
    Summary Line:
    Extract the important contents from questions_file and save meaningfully save it in a list

    Parameters:
    questions_file: Questions file that needs to be processed

    Returns:
    list of dictionaries: [{questionId:..., question:..., Difficulty:..., Type:...},{questionId:..., question:..., Difficulty:..., Type:...},{...}, ...]
    """
    file_content = read_questions_file(questions_file)

    question_pair_lst = find_question_components(file_content)

    question_pair_lst = add_question_type(question_pair_lst)

    return question_pair_lst

# question_details = process_questions_file("../developset-v2/1999-W03-5.questions")

# for entr in question_details:
#     print(entr)
