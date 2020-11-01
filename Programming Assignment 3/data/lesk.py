
import sys

def read(fileName):
    allSentenceList = []
    with open(fileName) as fp:
        for line in fp:
            allSentenceList.append(line.lower())
    return allSentenceList

def write(output_lst):
    with open("test.txt.lesk", "w") as fp:
        for i, sense_str in enumerate(output_lst):
            if i == len(output_lst)-1:
                fp.write("%s"%(sense_str.rstrip(" ")))
            else:
                fp.write("%s\n"%(sense_str.rstrip(" ")))
    

def constructSenseDict(sentenceList):
    senseSignatureDict = {}
    for line in sentenceList:
        sense_signature = line.split("\t", 1)
        sense = sense_signature[0]
        signature = sense_signature[1].split("\t",1)
        glossWordsLst = [word.lower() for word in signature[0].split()]
        exampleWordsLst = [word.lower() for word in signature[1].split()]
        
        signatureWordsSet = set(glossWordsLst) | set(exampleWordsLst)
        
        senseSignatureDict[sense] = signatureWordsSet
        
    return senseSignatureDict   

def constructStopWordsSet(stopWords):
    stopWordsSet = set()
    for word in stopWords:
        stopWordsSet.add(word.lower().strip("\n"))
    return stopWordsSet

def constructContextSet(sentence):
    contextWordsLst = sentence.split()
    contextSet = set()
    for word in contextWordsLst:
        contextSet.add(word.lower())
    return contextSet

def removeStopWords(senseDict,stopWordsSet):
    for sense, signature in senseDict.items():
            intersection = signature & stopWordsSet
            for word in intersection:
                signature.remove(word)
            senseDict[sense] = signature

def lesk(senseDict, sentence):
    leskDict = {}
    context = constructContextSet(sentence)

    for sense in senseDict:
        signature = senseDict[sense]
        overlap_words = signature & context
        # remove words that don't contain alphabets
        removeSet = set()
        for word in overlap_words:
            if not any(c.isalpha() for c in word):
                removeSet.add(word)
        for word in removeSet:
            overlap_words.remove(word)        
        overlap = len(overlap_words)
        
        leskDict[sense] = overlap
    ordered_items = sorted(leskDict.items(), key = lambda x:(-x[1], x[0]))
    return ordered_items

def generateOutputFormat(sentence):
    res_str = ""
    for word, overlap in sentence:
        res_str += word+"("+str(overlap)+") "
    res_str.strip(" ")
    return res_str

if __name__ == "__main__":
    conextFile, definitionsFile, stopwordsFile = sys.argv[1],sys.argv[2], sys.argv[3]

    definitionSentences = read(definitionsFile)
    contextSentences = read(conextFile)
    stopwordsSentences = read(stopwordsFile)
    
    senseDict = constructSenseDict(definitionSentences)
    stopWordsSet = constructStopWordsSet(stopwordsSentences)
    removeStopWords(senseDict, stopWordsSet)

    ouput_lst = []
    for sentence in contextSentences:
        # find the most meaningful sense
        sense_pair = lesk(senseDict, sentence)
        output_str = generateOutputFormat(sense_pair)
        ouput_lst.append(output_str)
    write(ouput_lst)
        
