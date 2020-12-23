clue = 3
good_clue = 4
confident = 6
slam_dunk = 20

all_question_type = {"why", "whose", "what",
                     "where", "when", "how", "who", "whom"}

# common prepositions: above, along, at, below, beside, between, during, for, from, in, near, on, outside, over, past, through, towards, under, up, with
location_preposition = {"in", "on", "at", "near", "next to", "between", "far from", "opposite", "behind", "under",
                        "below", "above", "on top of", "at the top", "at the bottom", "across", "beside", "around",
                        "front"}

spacy_location_labels = {"GPE", "LOC"}
date_time_labels = {"DATE", "TIME"}

usa_names_1910_2013 = []
with open('./data_files/usa_names_1910_2013', 'r') as names_file:
    usa_names_1910_2013 = names_file.readlines()
    usa_names_1910_2013 = set(
        map(lambda name: name.strip(), usa_names_1910_2013))

common_titles = []
with open('./data_files/common_titles.txt', 'r') as common_titles_file:
    common_titles = common_titles_file.readlines()
    common_titles = set(map(lambda name: name.strip(), common_titles))
# print(common_titles)

#common_last_names = []
#with open('./data_files/common_last_names.txt', 'r') as common_last_names_file:
#    common_last_names = common_last_names_file.readlines()
#    common_last_names = set(map(lambda name: name.strip().lower(), common_last_names))

#occupation_words = []
#with open('./data_files/occupation_words.txt', 'r') as occupation_words_file:
#    occupation_words = occupation_words_file.readlines()
#    occupation_words = set(map(lambda name: name.strip().lower(), occupation_words))

human_class = usa_names_1910_2013 | common_titles

countries = []
with open("./data_files/country_names.txt") as fp:
    country_names = fp.readlines()
    countries = list(map(lambda name: name.strip(), country_names))

us_states = []
with open("./data_files/states_US.txt") as fp:
    states = fp.readlines()
    us_states = list(map(lambda name: name.strip(), states))

canadian_provinces = []
with open("./data_files/provinces_CANADA.txt") as fp:
    provinces = fp.readlines()
    canadian_provinces = list(map(lambda name: name.strip(), provinces))

LOCATION = countries + us_states + canadian_provinces

MONTH = {"january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november",
         "december"}

quantifiers = {"feet", "mile", "tall", "big", "small", "short", "long", "much", "many", "majority", "large", "few", "several", "plently",
               "lot", "some", "none", "all", "cost", "money", "old", "young", "age", "million", "billion", "dollar", "year", "month", "percent"}

currency_symbols = {"$", "€", "£", "¥", }
