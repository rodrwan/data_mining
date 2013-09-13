#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import nltk, re, sys 
from collections import Counter
import numpy as np
from math import sqrt, pow
from tabulate import tabulate
from numpy.random import rand
from scipy.cluster.vq import kmeans, vq

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
    try:
        if len(sys.argv) < 2:
            raise NameError('>>> Faltan Parametros.')
        else:
            arch = sys.argv[1]
            fi =  open(arch, 'r')
            content = fi.readlines()
            globalWords = {}
            countINF, countNAV, countRES = 0.0, 0.0, 0.0
            querys, category = [], []

            for i in content:

                data = i.split('\t')
                if data[0] == 'INF':
                    countINF += 1
                elif data[0] == 'NAV':
                    countNAV += 1
                elif data[0] == 'RES':
                    countRES += 1
                category.append(data[0])
                querys.append(data[1].rstrip())
                tok = token(data[1].rstrip())
                query = []
                
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

            for glosa in querys:
                tok = token(glosa)
                arrQuery = [0]*len(bag_of_word)
                for j  in tok:
                    arrQuery[bag_of_word.index( j[0] )] = j[1]
                matrix.append(arrQuery)
            
            matrix = np.array(matrix)
            centroids, dist = kmeans(matrix, 3)
            idx, distanc = vq(matrix, centroids)
            inf = 0
            nav = 0
            res = 0
            categoryArray = []
            for i in idx:
                if i == 0:
                    categoryArray.append('INF')
                    inf += 1
                elif i == 1:
                    categoryArray.append('NAV')
                    nav += 1
                elif i == 2:
                    categoryArray.append('RES')
                    res += 1
            print
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
                        accuracyInf += 1
                    elif categoryArray[j] == 'NAV':
                        accuracyNav += 1
                    elif categoryArray[j] == 'RES':
                        accuracyRes += 1
                j += 1

            headers = ["Categoria", "Iniciales", "Obtenidos", "Correctos", "Incorrectos", "Accuracy", "Recall", "Precision", "F-Score"] #
            table = [
                [
                    "INF",
                    countINF,
                    inf,
                    accuracyInf,
                    inf-accuracyInf,
                    "{0:.2f}".format(accuracyInf/countINF), 
                    "{0:.2f}".format((inf-accuracyInf)/countINF), 
                    "{0:.2f}".format((inf-accuracyInf)/inf), 
                    "{0:.2f}".format(f_score((inf-accuracyInf)/inf, (inf-accuracyInf)/countINF, 1))
                ],
                [
                    "NAV", 
                    countNAV,
                    nav,
                    accuracyNav,
                    nav-accuracyNav,
                    "{0:.2f}".format(accuracyNav/countNAV), 
                    "{0:.2f}".format((nav-accuracyNav)/countNAV), 
                    "{0:.2f}".format((nav-accuracyNav)/nav), 
                    "{0:.2f}".format(f_score((nav-accuracyNav)/nav, (nav-accuracyNav)/countNAV, 1))
                ],
                [
                    "RES", 
                    countRES,
                    res,
                    accuracyRes,
                    res-accuracyRes,
                    "{0:.2f}".format(accuracyRes/countRES), 
                    "{0:.2f}".format((res-accuracyRes)/countRES), 
                    "{0:.2f}".format((res-accuracyRes)/res),
                    "{0:.2f}".format(f_score((res-accuracyRes)/res, (res-accuracyRes)/countRES, 1))
                ]
            ]
            print tabulate(table, headers, tablefmt="orgtbl")
            print
            print "Accuracy: {0:.2f}".format(accuracy/3000)
            print

            inf_inf, nav_inf, res_inf = 0.0, 0.0, 0.0
            inf_nav, nav_nav, res_nav = 0.0, 0.0, 0.0
            inf_res, nav_res, res_res = 0.0, 0.0, 0.0
            
            j = 0
            for i in content:
                tag = i.split('\t')[0]
                if tag == 'INF':
                    if categoryArray[j] == 'INF':
                        inf_inf += 1
                    elif categoryArray[j] == 'NAV':
                        nav_inf += 1 
                    elif categoryArray[j] == 'RES':
                        res_inf += 1
                
                elif tag == 'NAV':
                    if categoryArray[j] == 'INF':
                        inf_nav += 1
                    elif categoryArray[j] == 'NAV':
                        nav_nav += 1 
                    elif categoryArray[j] == 'RES':
                        res_nav += 1
                
                elif tag == 'RES':
                    if categoryArray[j] == 'INF':
                        inf_res += 1
                    elif categoryArray[j] == 'NAV':
                        nav_res += 1 
                    elif categoryArray[j] == 'RES':
                        res_res += 1
                j += 1
            
            print "Matriz de confusion:"
            headers = ["INF", "NAV", "RES", "Total"]
            table = [
                ["INF", inf_inf, nav_inf, res_inf, countINF],
                ["NAV", inf_nav, nav_nav, res_nav, countNAV],
                ["RES", inf_res, nav_res, res_res, countRES]
            ]
            print tabulate(table, headers, tablefmt="orgtbl")
            print

            sys.exit()
                   
    except Exception, e:
        print str(e)
        print
        print "Modo de uso:"
        print "python tokens.py [nombre archivo] [man|can|cor|chi]"
        print
    finally:
        fi.close()
    
