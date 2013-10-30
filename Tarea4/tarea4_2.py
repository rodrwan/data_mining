#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import nltk, re, sys 
from collections import Counter
import numpy as np
from math import sqrt, pow
from tabulate import tabulate
from numpy.random import rand
from scipy.cluster.vq import kmeans, vq
from nltk.tag.stanford import POSTagger
from nltk.tokenize import word_tokenize
path_to_model = 'C:/Users/rodrwan/Desktop/data mining/data_mining/Tarea4/stanford-postagger/models/left3words-wsj-0-18.tagger'
path_to_jar = 'C:/Users/rodrwan/Desktop/data mining/data_mining/Tarea4/stanford-postagger/stanford-postagger.jar'
st = POSTagger(path_to_model, path_to_jar)

def token(files):
    stop_words = [
        "a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the", ".", "?", "&", ":"
    ]
    data = files.lower()
    tokens = nltk.word_tokenize(data)
    final_tok = []
    for j in tokens:
        try:
            if stop_words.index(j) >= 0:
                pass
        except:
            final_tok.append(j)
    
    nonPunct = re.compile('.*[\W+\w+].*')
    filtered = [w for w in final_tok if nonPunct.match(w)]    
    counts = Counter(filtered)
    token = counts.items()

    return token #, len(counts)

def f_score(pres, recall, beta):
    numerador = pres*recall
    denominador = (pow(beta,2)*pres)+recall
    factor = 1+pow(beta, 2)
    try:
        return factor*(numerador/denominador)
    except:
        return 0

"""
PARTE PRINCIPAL PROGRAMA
"""
if __name__=="__main__":
    if len(sys.argv) < 2:
        raise NameError('>>> Faltan Parametros.')
    else:
        arch = sys.argv[1]
        fi =  open(arch, 'r')
        content = fi.readlines()
        category = []
        
        countINF, countNAV, countRES = 0.0, 0.0, 0.0
        S = []
        S_p = []
        querys = []
        for i in content:
            
            data = i.rstrip().split('\t')
            query = data[1]

            if data[0] == 'INF':
                countINF += 1
            elif data[0] == 'NAV':
                countNAV += 1
            elif data[0] == 'RES':
                countRES += 1
            
            category.append(data[0])
            querys.append(query)

        best_accuracy = []
        headers = ["Categorias", "Accuracy" ]#
        table = []
        X = ['NNP', 'NN', 'NNS', 'JJ', 'CD', 'VB']    
        
        X_p = ['NNP', 'NN', 'NNS', 'JJ', 'CD', 'VB']
        for i in X:
            for x in X_p:
                final_query = []
                if x not in S:
                    S_p = S + [x]
                                
                for query in querys:
                    datos = query.split(" ")

                    string = ''
                    k = ''
                    for s in S_p:
                        for d in datos:
                            if s in d:
                                string += d.split("/")[0] + " "
                    
                    final_query.append(string.rstrip())
                globalWords = {}
                querys_f = []
                for data in final_query: 
                    querys_f.append(data)
                    tok = token(data)
                   
                    for j in tok:
                        if str(j[0]) in globalWords:
                            globalWords[str(j[0])] += j[1]
                        else:
                            globalWords[str(j[0])] = j[1]

                bag_of_word, bag_of_word_num, bag_of_word_count = [], [], 0

                for word in globalWords.keys():
                    bag_of_word.append(word)
                    bag_of_word_count += globalWords[word]
                    bag_of_word_num.append(globalWords[word])

                matrix = []

                for glosa in querys_f:
                    tok = token(glosa)
                    arrQuery = [0]*len(bag_of_word)
                    for j  in tok:
                        arrQuery[bag_of_word.index( j[0] )] = j[1]
                    matrix.append(arrQuery)
                
                matrix = np.array(matrix)

                centroids, dist = kmeans(matrix, 3)
                idx, distanc = vq(matrix, centroids)
                inf = 0.
                nav = 0.
                res = 0.
                categoryArray = []
                for i in idx:
                    if i == 0:
                        categoryArray.append('INF')
                        inf += 1.
                    elif i == 1:
                        categoryArray.append('NAV')
                        nav += 1.
                    elif i == 2:
                        categoryArray.append('RES')
                        res += 1.
                
                j = 0
                accuracy = 0.0
                accuracyInf = 0.0
                accuracyNav = 0.0
                accuracyRes = 0.0

                for i in content:
                    etiqueta = i.split('\t')[0]
                    if etiqueta == categoryArray[j]:
                        accuracy += 1.0
                        if categoryArray[j] == 'INF':
                            accuracyInf += 1.
                        elif categoryArray[j] == 'NAV':
                            accuracyNav += 1.
                        elif categoryArray[j] == 'RES':
                            accuracyRes += 1.
                    j += 1
                best_accuracy.append( ( S_p[:], (accuracy/len(final_query)) ) )
                best = []
                for b in best_accuracy:
                    best.append(b[1])
                pos = 0
                max_best = max(best)
                
                for b in best_accuracy:
                    if b[1] == max_best:
                        break
                    else:
                        pos += 1

                S = best_accuracy[pos][0]
                
                for h in S:
                    try:
                        del X_p[X_p.index(h)]
                    except:
                        pass
                # print "S: " + str(S)
                # print "X: " + str(X_p)
                # print "A: " + str(accuracy/len(final_query))
                # print 
            table.append([ str(S), (accuracy/len(final_query)) ])
        print  
        print tabulate(table, headers, tablefmt="orgtbl")

            



            