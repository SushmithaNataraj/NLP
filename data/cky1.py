import sys, operator, copy
from collections import defaultdict

class ReadFile:
    def readSentences(self, fileName):
        allSentences = []
        with open(fileName) as fp:
            for line in fp:
                allSentences.append(line.strip("\n"))
        return allSentences    
        
    def readGrammar(self, fileName):
        grammar = {}
        with open(fileName) as fp:
            for line in fp:
                line = line.strip("\n")
                lhs, rhs = line.split("->", 1)
                rhsRules = tuple([rule.strip(" ") for rule in rhs.split(" ") if rule][:-1])
                lhs = lhs.strip()
                if rhsRules not in grammar:
                    grammar[rhsRules] = [lhs]
                else:
                    grammar[rhsRules].append(lhs)
        return grammar

result_cell_values = {}
class CKY:
    def searchInGrammar(self, prev_set, next_set, grammar, result_cell):
        res_set = set()
        # if result_cell:
        #     result_cell_values = {}
        global result_cell_values
        for rule_1 in prev_set:
            for rule_2 in next_set:  
                new_rule = (rule_1.strip(" "), rule_2.strip(" "))
                if new_rule in grammar:
                    res_set |= set(grammar[(new_rule)])
                    if result_cell and not new_rule in result_cell_values:
                        result_cell_values[new_rule] = grammar[new_rule]               
        return res_set

    def ckyGrid(self, sentence, grammar):
        words = sentence.split(" ")
        n = len(words)
        dp = []
        global result_cell_values
        for r in range(n):
            lst = []
            for c in range(n):
                lst.append(set())
            dp.append(lst)

        # Initialize all the diagonals with the rules
        for diag in range(n):
            # For each word, find the grammar rule for that word and add it to dp diagonal
            key = words[diag],
            if key in grammar:
                rules = grammar[key]
                for rule in rules:
                    dp[diag][diag].add(rule)
        parse_count = 0
        for c in range(1, n):
            for r in range(c-1, -1, -1):
                # print("Col:",c, "Row",r)
                for s in range(r+1, c+1):
                    result_cell = 1 if (c == n-1 and r == 0) else 0
                    prev_constituent_set = dp[r][s-1]
                    next_constituent_set =  dp[s][c]
                    # print("Update dp["+str(r)+"]["+str(c)+"]", dp[r][c],"by comparing","dp["+str(r)+"]["+str(s-1)+"]:", dp[r][s-1],"Against", "dp["+str(s)+"]["+str(c)+"]:", dp[s][c])
                    if prev_constituent_set and next_constituent_set:
                        res_set = self.searchInGrammar(prev_constituent_set, next_constituent_set, grammar, result_cell)
                        dp[r][c] |= res_set
                if c == n-1 and r == 0:
                    dp[r][c] = []
                    for values in result_cell_values.values():
                        for v in values:
                            if v == "S":
                                parse_count += 1
                            dp[r][c].append(v)
                    result_cell_values = {}             

        print("PARSING SENTENCE: "+sentence)
        i = 0
    
        print("NUMBER OF PARSES FOUND: "+str(parse_count))
        print("TABLE:")
        table = []
        
        for i in range(n):
            for j in range(i, n):
                dp[i][j] = sorted(dp[i][j])
                cell = " ".join(str(i) for i in dp[i][j]) if dp[i][j] else "-"
                cell_content = "Cell["+str(i+1)+","+str(j+1)+"]: " + cell
                table.append(cell_content)
                print(cell_content)
                
    def ckyAlgorithm(self, sentences, grammar):
        for sentence in sentences:
            self.ckyGrid(sentence, grammar)
            print("\n")       

if __name__ == "__main__":
    # print(sys.argv)
    pcfg = sys.argv[1]
    sentence = sys.argv[2]
    # print(pcfg, sentence)

    readObj = ReadFile()
    allSentences = readObj.readSentences(sentence)
    # print(allSentences)

    grammar = {}
    grammar = readObj.readGrammar(pcfg)
    # print("\n",grammar)

    cky = CKY()
    cky.ckyAlgorithm(allSentences, grammar)

  

