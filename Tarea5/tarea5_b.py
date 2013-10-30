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
    if len(sys.argv) < 2:
        raise NameError(">>> Faltan Parametros.")
    else:
        arch = sys.argv[1]
        fi   = open(arch, 'r')
        content = fi.readlines()
        countINF, countNAV, countRES = 0.0, 0.0, 0.0
        category = []

        for i in content:
            data = i.split('\t')
            if data[0] == "INF":
                countINF += 1
            elif data[0] == "NAV":
                countNAV += 1
            elif data[0] == "RES":
                countRES += 1
            if data[0] == "INF":
                category.append(1)
            elif data[0] == "NAV":
                category.append(2)
            elif data[0] == "RES":
                category.append(3)
        

        countINFres, countNAVres, countRESres = 0.0, 0.0, 0.0
        categoryres = []
        
        for j in range(1, 11):
            fi2  = open('results/result_'+ str(j) +'.txt', 'r')
            content = fi2.readlines()
            for i in content:
                data = i.split(' ')
                if data[0] == "1":
                    categoryres.append(1)
                elif data[0] == "2":
                    categoryres.append(2)
                elif data[0] == "3":
                    categoryres.append(3)
            fi2.close() 

    acurracy = 0.
    for i in range(0, len(category)):
        # print str(category[i]) + " " + str(categoryres[i])
        if (category[i] == categoryres[i]):
            acurracy += 1

    print "Acurracy: " + str(acurracy/3000)
    print 

    inf_inf, nav_inf, res_inf = 0.0, 0.0, 0.0
    inf_nav, nav_nav, res_nav = 0.0, 0.0, 0.0
    inf_res, nav_res, res_res = 0.0, 0.0, 0.0

    for i in range(0, len(category)):
        if category[i] == 1:
            if categoryres[i] == 1:
                inf_inf += 1.
            elif categoryres[i] == 2:
                nav_inf += 1.
            elif categoryres[i] == 3:
                res_inf += 1.
        
        elif category[i] == 2:
            if categoryres[i] == 1:
                inf_nav += 1.
            elif categoryres[i] == 2:
                nav_nav += 1.
            elif categoryres[i] == 3:
                res_nav += 1.
        
        elif category[i] == 3:
            if categoryres[i] == 1:
                inf_res += 1.
            elif categoryres[i] == 2:
                nav_res += 1.
            elif categoryres[i] == 3:
                res_res += 1.
    
    print "Matriz de confusion:"
    headers = ["INF", "NAV", "RES", "Total"]
    table = [
        ["INF", inf_inf, nav_inf, res_inf, countINF],
        ["NAV", inf_nav, nav_nav, res_nav, countNAV],
        ["RES", inf_res, nav_res, res_res, countRES]
    ]
    print tabulate(table, headers, tablefmt="orgtbl")
    print

