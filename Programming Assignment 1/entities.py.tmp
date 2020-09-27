import sys
from collections import OrderedDict
train_vec = []
test_vec = []

fwords = {"UNK":1, "PHI":2, "OMEGA":3}
fprev_word = {"UNK":4, "PHI":5, "OMEGA":6}
fnext_word = {"UNK":7, "PHI":8, "OMEGA":9}

fpos = {"UNKPOS":10, "PHIPOS":11, "OMEGAPOS":12}
fprev_pos = {"UNKPOS":13, "PHIPOS":14, "OMEGAPOS":15}
fnext_pos = {"UNKPOS":16, "PHIPOS":17, "OMEGAPOS":18}
fcap, fabbr = {},{}
fcap["CAP"] = 19
fabbr["ABBR"] = 20

flabel = {"O": 0, "B-PER": 1, "I-PER": 2,
          "B-LOC": 3, "I-LOC": 4, "B-ORG": 5, "I-ORG": 6}

global_counter = 20
def increment():
    global global_counter
    global_counter += 1
    return global_counter


class ReadFileData:
    def read_file(self, file_name):
        t_doc = []
        with open(file_name) as fp:
            lst = []
            for i, line in enumerate(fp):
                # if i == 50:
                #     break
                line = line.rstrip('\n')
                if not line:
                    if lst:
                        t_doc.append(lst)
                        lst = []
                else:
                    lst.append(line)

            if lst:
                t_doc.append(lst)
        return t_doc

class WriteToFile:
    def write_file(self, word_doc, file_name, is_file_last_line):
        try:
            with open(file_name, "a") as fp:
                for ftype, value in word_doc.items():
                    fp.write("%s\n" % (str(ftype)+": "+value))
                if not is_file_last_line:
                    fp.write("\n")
        except IOError:
            with open(file_name, "w") as fp:
                for ftype, value in word_doc.items():
                    fp.write("%s\n" % (str(ftype)+": "+value))
                if not is_file_last_line:
                    fp.write("\n")

class WriteToBinaryFeatureFile:
    def write_file(self, binary_doc, file_name):
        with open(file_name, "a") as fp:
            for line in binary_doc:
                fp.write("%s\n" % line)
       
class GenerateReadableWordDocTrain:
    def is_cap(self, word):
        return word[0].isupper()

    def is_abbr(self, word):
        contains_alpha = 0
        if len(word) > 4:
            return 0
        if word[-1] != '.':
            return 0
        for char in word:
            if not char.isalpha() and char != '.':
                return False
            if char.isalpha():
                contains_alpha = 1

        return contains_alpha

    def find_wordcon(self, i, word, sentence):  
        prev, next_ = '', ''
        if i == 0:
            prev = "PHI"
            if i+1 == len(sentence):
                next_ = "OMEGA"
            else:
                next_ = [k for k in sentence[i+1].split(" ") if k][-1]

        elif i == len(sentence) - 1:
            prev = [k for k in sentence[i-1].split(" ") if k][-1]
            next_ = "OMEGA"
        elif i > 0 and i < len(sentence) - 1:
            prev = [k for k in sentence[i-1].split(" ") if k][-1] 
            next_ = [k for k in sentence[i+1].split(" ") if k][-1]

        if prev not in fprev_word:
            fprev_word[prev] = increment()
        if next_ not in fnext_word:
            fnext_word[next_] = increment()       
        return prev+" "+next_

    def find_poscon(self, i, word, sentence, unique_obj = None):
        prev, next_ = '', ''
        if i == 0 and i < len(sentence) - 1:
            prev = "PHIPOS"
            # next_ = sentence[i+1].split(" ")[2]
            next_ = [k for k in sentence[i+1].split(" ") if k][1]
        elif i == len(sentence) - 1 and i > 0:
            # prev = sentence[i-1].split(" ")[2]
            prev = [k for k in sentence[i-1].split(" ") if k][1]
            next_ = "OMEGAPOS"
        elif i > 0 and i < len(sentence) - 1:
            # prev = sentence[i-1].split(" ")[2]
            # next_ = sentence[i+1].split(" ")[2]
            prev = [k for k in sentence[i-1].split(" ") if k][1]
            next_ = [k for k in sentence[i+1].split(" ") if k][1]
        if unique_obj:
            if prev not in unique_obj.pos:
                prev = "UNKPOS"
            if next_ not in unique_obj.pos:
                next_ = "UNKPOS"
        if prev not in fprev_pos:
            fprev_pos[prev] = increment()
        if next_ not in fnext_pos:
            fnext_pos[next_] = increment()

        return prev+" "+next_


    def generate_doc(self, i, each_word_entr, sentence, ftype):

        word_doc = OrderedDict({"WORD": "n/a", "POS": "n/a", "ABBR": "n/a",
                                "CAP": "n/a", "WORDCON": "n/a", "POSCON": "n/a"})
        line = [k for k in each_word_entr.split(" ") if k]
        pos, word = line[1], line[2]
        word_doc["WORD"] = word

        if ftype["POS"]:
            word_doc["POS"] = pos

        if ftype["ABBR"]:
            word_doc["ABBR"] = "yes" if self.is_abbr(word) else "no"

        if ftype["CAP"]:
            word_doc["CAP"] = "yes" if self.is_cap(word) else "no"

        if ftype["WORDCON"]:
            word_doc["WORDCON"] = self.find_wordcon(i, word, sentence)
        if ftype["POSCON"]:
            word_doc["POSCON"] = self.find_poscon(i, word, sentence)

        return word_doc


class GenerateReadableWordDocTest:
    def is_cap(self, word):
        return word[0].isupper()

    def is_abbr(self, word):
        contains_alpha = 0
        if len(word) > 4:
            return 0
        if word[-1] != '.':
            return 0
        for char in word:
            if not char.isalpha() and char != '.':
                return False
            if char.isalpha():
                contains_alpha = 1

        return contains_alpha

    def find_wordcon(self, i, word, sentence, all_words):   
        prev, next_ = '', ''

        # ONly word
        if i == 0:
            if i + 1 == len(sentence):
                return "PHI OMEGA"
            else:
                prev = "PHI"
                next_ = [k for k in sentence[i+1].split(" ") if k][-1]
                if next_ not in all_words:
                    next_ = "UNK"
                return prev + " "+next_
        # last woed-rd
        elif i == len(sentence) - 1:
            prev = [k for k in sentence[i-1].split(" ") if k][-1]
            next_ = "OMEGA"
            if prev not in all_words:
                prev = "UNK"
            return prev + " "+ next_
        else:
            prev = [k for k in sentence[i-1].split(" ") if k][-1] 
            if prev not in all_words:
                prev = "UNK"

            next_ = [k for k in sentence[i+1].split(" ") if k][-1]
            if next_ not in all_words:
                next_ = "UNK" 


            return prev+" "+next_

    def find_poscon(self, i, word, sentence, all_pos):
        prev, next_ = '', ''
        if i == 0:
            prev = "PHIPOS"
            if i+1 == len(sentence):
                next_ = "OMEGAPOS"
            else:
                next_ = [k for k in sentence[i+1].split(" ") if k][1]
                if next_ not in all_pos:
                    next_ = "UNKPOS"
            return prev + " " + next_

        elif i == len(sentence) - 1:
            next_ = "OMEGAPOS"
            prev = [k for k in sentence[i-1].split(" ") if k][1]
            if prev not in all_pos:
                prev = "UNKPOS"
            return prev + " "+next_

        elif i > 0 and i < len(sentence) - 1:
            prev = [k for k in sentence[i-1].split(" ") if k][1]
            if prev not in all_pos:
                prev = "UNKPOS"

            next_ = [k for k in sentence[i+1].split(" ") if k][1]
            if next_ not in all_pos:
                next_ = "UNKPOS"
        
            return prev+" "+next_


    def generate_doc(self, i, each_word_entr, sentence, ftype, all_words, all_pos):

        word_doc = OrderedDict({"WORD": "UNK", "POS": "n/a", "ABBR": "n/a",
                                "CAP": "n/a", "WORDCON": "n/a", "POSCON": "n/a"})
        line = [k for k in each_word_entr.split(" ") if k]
        pos, word = line[1], line[2]
        if word in all_words:
            word_doc["WORD"] = word

        if ftype["POS"]:
            if pos in all_pos:
                word_doc["POS"] = pos
            else:
                word_doc["POS"] = "UNKPOS"

        if ftype["ABBR"]:
            word_doc["ABBR"] = "yes" if self.is_abbr(word) else "no"

        if ftype["CAP"]:
            word_doc["CAP"] = "yes" if self.is_cap(word) else "no"

        if ftype["WORDCON"]:
            word_doc["WORDCON"] = self.find_wordcon(i, word, sentence, all_words)
        if ftype["POSCON"]:
            word_doc["POSCON"] = self.find_poscon(i, word, sentence, all_pos)
        return word_doc


class Process_train_lst:
    
    def process_train_lst(self, train_doc, ftype):
        all_train_words = set()
        all_train_pos = set()
        for row_index, sentence in enumerate(train_doc):
            for i, each_word_entr in enumerate(sentence):
                
                #Generate word doc
                word_doc_obj = GenerateReadableWordDocTrain()
                word_doc = word_doc_obj.generate_doc(i, each_word_entr, sentence, ftype)

                # As soon as you get all the 6 values for a word doc, write to to file
                is_file_last_line = 0
                if row_index == len(train_doc) - 1 and i == len(sentence) - 1:
                    is_file_last_line = 1

                #write it to human readable file
                write_obj = WriteToFile()
                write_obj.write_file(word_doc, "trainE.txt.readable", is_file_last_line)

                #split the line and get POS and word
                line = [k for k in each_word_entr.split(" ") if k]
                label, pos, word = line[0],line[1], line[2]

                all_train_words.add(word)
                all_train_pos.add(pos)
                

                if word not in fwords:
                    fwords[word] = increment()

                if pos not in fpos:
                    fpos[pos] = increment()
                # if row_index < 1 and i < 5:
                #     print("WORD:", word,fwords[word], "POS:", pos,fpos[pos])

                train_feature_id = [fwords[word]]
                if ftype["POS"]:
                    train_feature_id.append(fpos[pos])
                if ftype["WORDCON"] and word_doc["WORDCON"] != "n/a":
                    wordcon_value = word_doc["WORDCON"].split(" ")
                    prev = wordcon_value[0]
                    next_ = wordcon_value[1]
                    train_feature_id.append(fprev_word[prev])
                    train_feature_id.append(fnext_word[next_])
                    # if row_index < 1 and i < 5:
                    #     print("WORDCON:", fprev_word[prev], fnext_word[next_])
                        
                if ftype["POSCON"] and word_doc["POSCON"] != "n/a":
                    poscon_value = word_doc["POSCON"].split(" ")
                    prev = poscon_value[0]
                    next_ = poscon_value[1]
                    train_feature_id.append(fprev_pos[prev])
                    train_feature_id.append(fnext_pos[next_])
                    # if row_index < 1 and i < 5:
                    #     print("POSCON:", fprev_pos[prev], fnext_pos[next_])
                if ftype["CAP"] and word_doc["CAP"] == "yes":
                    train_feature_id.append(fcap["CAP"])
                if ftype["ABBR"] and word_doc["ABBR"] == "yes":
                    train_feature_id.append(fabbr["ABBR"])

                train_feature_id.sort()
                cur_vector = str(flabel[label])
                
                for item in train_feature_id:
                    cur_vector += " "+ str(item)+":1"
                train_vec.append(cur_vector)

                


        
        return all_train_words, all_train_pos

class ProcessTestLst:
    def process_test_lst(self, test_doc, all_words, all_pos):
        for row_index, sentence in enumerate(test_doc):
            for i, each_word_entr in enumerate(sentence):
                #Generate word doc
                word_doc_obj = GenerateReadableWordDocTest()
                word_doc = word_doc_obj.generate_doc(i, each_word_entr, sentence, ftype, all_words, all_pos)

                is_file_last_line = 0
                if row_index == len(test_doc) - 1 and i == len(sentence) - 1:
                    is_file_last_line = 1

                write_obj = WriteToFile()
                write_obj.write_file(word_doc, "testE.txt.readable", is_file_last_line)


class BuildTestVector:
    def processTestDoc(self, test_doc, ftype):
        for row_index, sentence in enumerate(test_doc):
            for i, each_word_entr in enumerate(sentence):
                word_doc_obj = GenerateReadableWordDocTest()
                word_doc = word_doc_obj.generate_doc(i, each_word_entr, sentence, ftype, all_words, all_pos)
                line = [k for k in each_word_entr.split(" ")if k]
                label, pos, word = line[0], line[1], line[2]
                test_feature_id = []
                word = word_doc["WORD"]
                test_feature_id.append(fwords[word])
                if ftype["POS"]:
                    test_feature_id.append(fpos[word_doc["POS"]])
                if ftype["CAP"] and word_doc["CAP"] == "yes":
                    test_feature_id.append(fcap["CAP"])
                if ftype["ABBR"] and word_doc["ABBR"] == "yes":
                    test_feature_id.append(fabbr["ABBR"])
                if ftype["WORDCON"]:
                    wordcon_value = word_doc["WORDCON"].split(" ")
                    prev, next_ = wordcon_value[0], wordcon_value[1]
                    if prev in fprev_word:
                        test_feature_id.append(fprev_word[prev])
                    else:
                        test_feature_id.append(fprev_word["UNK"])
                    if next_ in fnext_word:
                        test_feature_id.append(fnext_word[next_])
                    else:
                        test_feature_id.append(fnext_word["UNK"])
                if ftype["POSCON"]:
                    poscon_value = word_doc["POSCON"].split(" ")
                    prev, next_ = poscon_value[0], poscon_value[1]
                    if prev in fprev_pos:
                        test_feature_id.append(fprev_pos[prev])
                    else:
                        test_feature_id.append(fprev_pos["UNKPOS"])
                    if next_ in fnext_pos:
                        test_feature_id.append(fnext_pos[next_])
                    else:
                        test_feature_id.append(fnext_pos["UNKPOS"])

                test_feature_id.sort()
                cur_vector = str(flabel[label])
                for item in test_feature_id:
                    cur_vector += " "+str(item)+":1"
                test_vec.append(cur_vector)
                
            

if __name__ == "__main__":
    train_file, test_file = sys.argv[1], sys.argv[2]
    ftype = {"WORD": 0, "POS": 0, "ABBR": 0,
             "CAP": 0, "WORDCON": 0, "POSCON": 0}

    for feature in sys.argv[3:]:
        if feature in ftype:
            ftype[feature] = 1


    read_obj = ReadFileData()
    train_document_lst = read_obj.read_file(train_file)
    test_document_lst = read_obj.read_file(test_file)

    readable_obj = Process_train_lst()
    all_words, all_pos = readable_obj.process_train_lst(train_document_lst, ftype)

    # for item in train_vec[:5]:
    #     print(item)
        
    readable_obj_test = ProcessTestLst()
    readable_obj_test.process_test_lst(test_document_lst, all_words, all_pos)

    build_test_vector = BuildTestVector()
    build_test_vector.processTestDoc(test_document_lst, ftype)

    feature_ob = WriteToBinaryFeatureFile()
    feature_ob.write_file(train_vec, "trainE.txt.vector")
    feature_ob.write_file(test_vec, "testE.txt.vector")
    