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

    def readPCFGGrammar(self, fileName):
        grammar = {}
        with open (fileName) as fp:
            for line in fp:
                line = line.strip("\n")
                lhs, rhs = line.split("->", 1)
                lhs = lhs.strip()
                rhsRules = [rule.strip(" ") for rule in rhs.split(" ") if rule]
                prob = rhsRules[-1]
                key = tuple(rhsRules[:-1])
                
                if key not in grammar:
                    grammar[key] = [[lhs, prob]]
                else:
                    grammar[key].append([lhs, prob])
            return grammar

result_cell_values = {}
class CKY:
    def searchInGrammar(self, prev_set, next_set, grammar, result_cell):
        res_set = set()
        # print(prev_set, next_set)
        # if result_cell:
        #     result_cell_values = {}
        global result_cell_values
        for rule_1 in prev_set:
            for rule_2 in next_set:  
                # print(rule_1, rule_2)
                new_rule = (rule_1.strip(" "), rule_2.strip(" "))
                if new_rule in grammar:
                    # print(grammar[new_rule], new_rule)
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
        for i in range(n):
            # For each word, find the grammar rule for that word and add it to dp diagonal
            key = words[i],
            if key in grammar:
                rules = grammar[key]
                # print(key, rules)
                for rule in rules:
                    dp[i][i].add(rule)
        # print(dp)
        parse_count = 0
        for c in range(1, n):
            for r in range(c-1, -1, -1):
                # print("Col:",c, "Row",r)
                for s in range(r+1, c+1):
                    
                    result_cell = 1 if (c == n-1 and r == 0) else 0
                    prev_constituent_set = dp[r][s-1]
                    next_constituent_set =  dp[s][c]
                    # print(r, c, prev_constituent_set, next_constituent_set)
                    # print("Update dp["+str(r)+"]["+str(c)+"]", dp[r][c],"by comparing","dp["+str(r)+"]["+str(s-1)+"]:", dp[r][s-1],"Against", "dp["+str(s)+"]["+str(c)+"]:", dp[s][c])
                    if prev_constituent_set and next_constituent_set:
                        # print(r,c)
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

class PCKY:
    def pckyAlgorithm(self, sentences, grammar):
        for sentence in sentences:
            self.pckyGrid(sentence, grammar) 
            # break
            print("\n")
    
    def searchInGrammar(self, prev_dict, next_dict, grammar,res_dict, result_cell):
        # res_dict = defaultdict(float)
        # print(grammar)
        global result_cell_values
        # print(prev_dict, next_dict)
        for rule_1, prob1 in prev_dict.items():
            for rule_2, prob2 in next_dict.items():  
                # print(rule_1,":", prob1, rule_2,":", prob2)
                new_rule = (rule_1.strip(" "), rule_2.strip(" "))
                # print("The new rule",new_rule, "Is in grammer?", new_rule in grammar)
                if new_rule in grammar:
                    result = grammar[(new_rule)]
                    # print(result)
                    for res in result:
                        rule, prob = res[0], res[1]
                        
                        updated_prob =float(format((round(float(prob) * float(prob1) * float(prob2), 4)), '.4f'))
                        res_dict[rule] = max(res_dict[rule], updated_prob)
                #     res_set |= set(grammar[(new_rule)])
                #     if result_cell and not new_rule in result_cell_values:
                #         result_cell_values[new_rule] = grammar[new_rule]               
        return res_dict
        
        pass
    
    def pckyGrid(self, sentence, grammar):
        # print(sentence)
        # print(grammar)
        words = sentence.split(" ")
        n = len(words)
        dp = []
        global result_cell_values
        for r in range(n):
            lst = []
            for c in range(n):
                lst.append({})
            dp.append(lst)

        # Initialize all the diagonals with the rules and probabilities
        for i in range(n):
            # For each word, find the grammar rule for that word and add it to dp diagonal
            key = words[i],
            if key in grammar:
                rules_and_prob = grammar[key]
                # print(key, rules_and_prob)
                for (rule,prob) in rules_and_prob:
                    dp[i][i][rule] = prob
        # print("\n",dp)
        parse_count = 0
        for c in range(1, n):
            for r in range(c-1, -1, -1):
                result_dict = defaultdict(float)
                # print("Col:",c, "Row",r)
                for s in range(r+1, c+1):
                    result_cell = 1 if (c == n-1 and r == 0) else 0
                    prev_constituent_dict = dp[r][s-1]
                    next_constituent_dict =  dp[s][c]
                    # print(r, c, prev_constituent_dict, next_constituent_dict)
                    # print("Update dp["+str(r)+"]["+str(c)+"]", dp[r][c],"by comparing","dp["+str(r)+"]["+str(s-1)+"]:", dp[r][s-1],"Against", "dp["+str(s)+"]["+str(c)+"]:", dp[s][c])
                    if prev_constituent_dict and next_constituent_dict:
                        # print(r, c)
                        self.searchInGrammar(prev_constituent_dict, next_constituent_dict, grammar,result_dict, result_cell)
                #         dp[r][c] |= res_set
                for k, v in result_dict.items():
                    dp[r][c][k] = v 
            if c == n-1 and r == 0:
                parse_count = 1 if "S" in dp[r][c] else 0
            
        # print(dp)
        print("PARSING SENTENCE: "+sentence)    
        print("NUMBER OF PARSES FOUND: "+str(parse_count))
        print("TABLE:")
        table = []
        for i in range(n):
            for j in range(i, n):
                dp[i][j] = sorted(dp[i][j].items(), key = operator.itemgetter(0))
                cell = ''
                if dp[i][j]:
                    for (r,p) in dp[i][j]:
                        p = format(float(p), '.4f')
                        cell += r + "("+p +") "
                else:
                    cell = '-'
            
                # cell = " ".join(str(i) for i in dp[i][j]) if dp[i][j] else "-"
                
                cell_content = "Cell["+str(i+1)+","+str(j+1)+"]: " + cell
                table.append(cell_content)
                print(cell_content)
                
                            





if __name__ == "__main__":
    # print(sys.argv)
    pcfg = sys.argv[1]
    sentence = sys.argv[2]
    # print(pcfg, sentence)
    pcky = 0
    if len(sys.argv) == 4:
        pcky = 1

    readObj = ReadFile()
    allSentences = readObj.readSentences(sentence)
    # print(allSentences)

    grammar = {}
    if not pcky:
        grammar = readObj.readGrammar(pcfg)
        # print("\n",grammar)

        cky = CKY()
        cky.ckyAlgorithm(allSentences, grammar)
    else:
        grammar = readObj.readPCFGGrammar(pcfg)
        pcky = PCKY()
        pcky.pckyAlgorithm(allSentences, grammar)

