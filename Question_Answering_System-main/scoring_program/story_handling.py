from nltk.tokenize import sent_tokenize
from parser import morphological_roots, word_tokenizer


def read_story_file(story_file):
    """
    """
    with open(story_file) as fp:
        file_content = fp.readlines()
    fp.close()
    return file_content
    

def process_story(story_lines):
    """
    Summary Line:
    Returns a list of sentences in the story

    Parameters:
    story_lines(list): A list containing each line in the story file

    Returns:
    list: A list containnig story sentences.
    """

    story_sentences = []
    story_headline = story_lines[0].strip()
    story_date = story_lines[1].strip()
    story_id = story_lines[2].strip()

    story_line_no = 3
    while story_lines[story_line_no].strip() != "TEXT:":
        story_line_no = story_line_no + 1
    story_line_no = story_line_no + 1
    story = ''.join(story_lines[story_line_no:])
    story_sentences = sent_tokenize(story)
    return story_sentences


def find_story_sentences(story_file):
    """
    Summary Line:
    Returns a list of sentences in the story

    Parameters:
    story_lines(list): A list containing each line in the story file

    Returns:
    list: A list containnig story sentences.
    """
    story_file_content = read_story_file(story_file)
    story_sentences = process_story(story_file_content)
    return story_sentences


def morph_story_sentences(story_file_path):
    """

    :param story_file_path: File path to the story
    :return: dict containing the sentence number as the key and the list as value.
            list is the original sentence of story and the morphological equivalent words of the sentence
    """
    story_sentences = find_story_sentences(story_file_path)
    morph_story_sentence = {}
    for index, sentence in enumerate(story_sentences):
        sentence_words = word_tokenizer(sentence)
        morph_sentence_words = morphological_roots(sentence_words)
        morph_story_sentence[index] = [sentence, morph_sentence_words]
    return morph_story_sentence
