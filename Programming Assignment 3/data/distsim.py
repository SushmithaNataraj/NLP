import sys, collections, numpy as np

vocabSet = set()
senseInventory = set()
sense_sentence_map = collections.defaultdict(list)
signature_vector_train = {}
signature_vector_test = {}
answer_tuple = []

def readFile(fileName):
    all_sentences = []
    with open(fileName) as fp:
        for line in fp:
            all_sentences.append(line.lower().strip("\n"))
    return all_sentences

def write(out_str, n, t):
    with open("test.txt.distsim", "w") as fp:
        fp.write("%s\n"%("Number of Training Sentences = "+str( n)))
        fp.write("%s\n"%("Number of Test Sentences = "+str(t)))
        fp.write("%s\n"%("Number of Gold Senses = "+str(len(senseInventory))))
        fp.write("%s\n"%("Vocabulary Size = "+str(len(vocabSet))))
        for i, line in enumerate(out_str):
            if i == len(out_str) - 1:
                fp.write("%s"%(line.rstrip(" ")))
            else:
                fp.write("%s\n"%(line.rstrip(" ")))

def generateOutputFormat(sentences):
    output = []
    
    for sentence in sentences:
        res_str = ""
        for (sense, sim) in sentence:
            sim =  "{0:.2f}".format(sim)
            res_str += sense+"("+sim+") "
        res_str.strip(" ")
        output.append(res_str)
    return output


def generateVocabulary(trainSentences, stopWords, k):
    words_freq_map = collections.defaultdict(int)
        
    global vocabSet, senseInventory, sense_sentence_map
    for i, sentence in enumerate(trainSentences):
        goldSenseSentence = sentence.split("\t", 1)

        goldSense = goldSenseSentence[0].split(":")[1]
        senseInventory.add(goldSense)

        sentence_without_sense = goldSenseSentence[1]
        wordsList = sentence_without_sense.split()
        
        sense_sentence_map[goldSense].append(sentence_without_sense)

        # Find the target word and its index
        for index, targetWord in enumerate(wordsList):
            if targetWord.startswith("<occurrence>") and targetWord.endswith("</>"):
                leftIndex = 0 if (index - k < 0 ) else index - k
                rightIndex = len(wordsList) if (index+k+1 > len(wordsList))else index + k + 1
                if k == 0:
                    leftIndex = 0
                    rightIndex = len(wordsList)
                leftWindow = wordsList[leftIndex:index]
                rightWindow = wordsList[index+1:rightIndex]
                for word in leftWindow:
                    words_freq_map[word] += 1
                for word in rightWindow:
                    words_freq_map[word] += 1
                    
        
        for word, freq in words_freq_map.items():
            if word not in stopWords and any (c.isalpha() for c in word) and freq > 1:
                vocabSet.add(word)

    # print( len(vocabSet))

def generateSignatureVectorTrain(k):
    for sense in sense_sentence_map:
        sentences = sense_sentence_map[sense]
        context_map = collections.defaultdict(int)
        
        # For all the sentences in this sense, collect the context map
        for sentence in sentences:
            wordsList = sentence.split()
            for index, targetWord in enumerate(wordsList):
                # Collect the context aroung the target word
                if targetWord.startswith("<occurrence>") and targetWord.endswith("</>"):
                    leftIndex = 0 if  (index - k < 0) else index - k
                    rightIndex = len(wordsList) if (index+k+1 > len(wordsList)) else index + k + 1
                    
                    if k == 0:
                        leftIndex = 0
                        rightIndex = len(wordsList)

                    leftWindow = wordsList[leftIndex:index]
                    rightWindow = wordsList[index+1:rightIndex]

                    window = leftWindow + rightWindow
                    window_counter = collections.Counter(window)
                    for word, freq in window_counter.items():
                        context_map[word] += freq

                    # break
        
        # From the context, generate signature vecor for this sense.
        vocab_counter = collections.Counter(vocabSet)
        for key in vocab_counter:
            vocab_counter[key] = context_map[key] if key in context_map else 0
        
        signature_vector = sorted(vocab_counter.items()) 
        signature_vector_train[sense] = signature_vector
        
        
    # print(signature_vector_train)

def generateSignatureVectorTest(testSentences, k):
    
    for i, sentence in enumerate(testSentences):
        context_map = collections.defaultdict(int)

        wordsList = sentence.split()
        for index, targetWord in enumerate(wordsList):
            if targetWord.startswith("<occurrence>") and targetWord.endswith("</>"):
                # print("Value of k ", k)
                leftIndex = 0 if (index - k < 0) else index - k
                rightIndex = len(wordsList) if (index+k+1 > len(wordsList)) else index + k + 1
                if k == 0:
                    leftIndex = 0
                    rightIndex = len(wordsList)

                leftWindow = wordsList[leftIndex:index]
                rightWindow = wordsList[index+1:rightIndex]
                
                
                window = leftWindow + rightWindow
                window_counter = collections.Counter(window)
                for word, freq in window_counter.items():
                    context_map[word] += freq

        vocab_counter = collections.Counter(vocabSet)
        # print(context_map)
        for key in vocab_counter:
            vocab_counter[key] = context_map[key] if key in context_map else 0
        # print(vocab_counter)
        # print("______________________________________________")
        signature_vector = sorted(vocab_counter.items()) 
        signature_vector_test[i] = signature_vector

def cosineSimilarity():
    global answer_tuple
    
    for index in signature_vector_test:
        signature_vector_y = signature_vector_test[index]
        
        y = [item[1] for item in signature_vector_y]
        
        cur_sentence = []
        
        for sense in senseInventory:
            signature_vector_x = signature_vector_train[sense]
            x = [item[1] for item in signature_vector_x]
        
            
            numerator = 0
            # numerator = np.dot(x, y)
            # denominator = np.linalg.norm(x) * np.linalg.norm(x)
            for i, j in zip(x,y):
                numerator += (i*j)
            # print(numerator)
            denominator_first_term = sum([n*n for n in x])**0.5
            denominator_sec_term = sum([n*n for n in y]) ** 0.5
            denominator = denominator_first_term * denominator_sec_term
            # print(numerator, denominator)
            cosine = 0.00 if not denominator else numerator/denominator
        
            cur_sentence.append((sense, cosine))
        cur_sentence.sort(key = lambda x:(-x[1], x[0]))
        answer_tuple.append(cur_sentence)

if __name__ ==  "__main__":
    trainFile, testFile, stopWords, k = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])

    trainSentences = readFile(trainFile)

    stopWords = set(readFile(stopWords))

    testSentences = readFile(testFile)

    generateVocabulary(trainSentences, stopWords, k)

    generateSignatureVectorTrain(k)

    generateSignatureVectorTest(testSentences, k)

    cosineSimilarity()
    output_lst = generateOutputFormat(answer_tuple)
    # print(output_lst)
    write(output_lst, len(trainSentences), len(testSentences))
    

    
