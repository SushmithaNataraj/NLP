import sys
import math

'''
TrainData will process the input train file. generates feature vector for the input train file
'''
class FileData:

    # Reads the training file and appends each line as a list to t_doc list
    def read_file(self, file_name):
        t_doc = []
        with open(file_name) as fp:
            lst = []
            for i, line in enumerate(fp):
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
            
'''
Features class will have a method to return top k feature words from feature file
'''
class Features:
    def __init__(self, feature_f, k):
        self.feature_file = feature_f
        self.k = k
    def vocabulary(self):
        with open(self.feature_file, "r") as fp:
            words = [next(fp).rstrip('\n') for i in range(self.k)]
        return words

class GenerateVector:
    def generate_vector(self, words, t_doc):
        t_vector = []
        for sentence in t_doc:
            class_ = sentence[0]
            cur_vector = class_
            for index, word in enumerate(words):
                if word in sentence[1:]:
                    cur_vector += " " + str(index+1) + ":" + '1'

            t_vector.append(cur_vector)
            cur_vector = ''

        return t_vector

class GenerateFile:
    def writeToFile(self, vectors, file_name):
        with open(file_name, "w") as fp:
            for each_vector in vectors:
                fp.write("%s\n"%(each_vector))


if __name__ == "__main__":
    train_file, test_file, feature_file, k = sys.argv[1], sys.argv[2],sys.argv[3], int(sys.argv[4])

    # k_words will have top k words from feature file list
    feature_obj = Features(feature_file, k)
    k_words = feature_obj.vocabulary()


    file_ptr = FileData()
    train_document = file_ptr.read_file(train_file)
    test_document = file_ptr.read_file(test_file)

    vector = GenerateVector()

    train_vector = vector.generate_vector(k_words, train_document)
    test_vector = vector.generate_vector(k_words, test_document)
    

    write_fp = GenerateFile()
    write_fp.writeToFile(train_vector, "trainS.txt.vector")
    write_fp.writeToFile(test_vector, "testS.txt.vector")


