#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import nltk, re, sys 
from collections import Counter
import numpy as np
from math import sqrt, pow
from tabulate import tabulate
from numpy.random import rand
from scipy.cluster.vq import kmeans, vq
import numpy;
import scipy;
import nltk;

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

def mintag(x, y, z):
    minimum = min(x, y, z)
    if x == minimum:
        return "INF"
    elif y == minimum:
        return "NAV"
    elif z == minimum:
        return "RES"

def test_maxent(algorithms, train, test):
    classifiers = {}
    try:
        classifiers[algorithms] = nltk.MaxentClassifier.train(train, algorithms, max_iter=2)
    except Exception, e:
        classifiers[algorithm] = e
    for algorithm, classifier in classifiers.items():
        # print '%11s' % algorithm,
        if isinstance(classifier, Exception):
            print 'Error: %r' % classifier; continue
        tag_results = []  
        for featureset in test:
            pdist = classifier.prob_classify(featureset)
            # print '%s%6.2f%6.2f%6.2f' % (mintag(pdist.prob('INF'), pdist.prob('NAV'), pdist.prob('RES')), pdist.prob('INF'), pdist.prob('NAV'), pdist.prob('RES'))
            tag_results.append( mintag( pdist.prob('INF'), pdist.prob('NAV'), pdist.prob('RES') ) )
        return tag_results
"""
PARTE PRINCIPAL PROGRAMA
"""
if __name__=="__main__":
    if len(sys.argv) < 2:
        raise NameError(">>> Faltan Parametros.")
    else:
        arch = sys.argv[1]
        fi =  open(arch, 'r')
        content = fi.readlines()
        globalWords = {}
        countINF, countNAV, countRES = 0.0, 0.0, 0.0
        querys, category = [], []

        for i in content:

            data = i.split('\t')
            if data[0] == "INF":
                countINF += 1
            elif data[0] == "NAV":
                countNAV += 1
            elif data[0] == "RES":
                countRES += 1
            if data[0] == "INF":
                category.append("INF")
            elif data[0] == "NAV":
                category.append("NAV")
            elif data[0] == "RES":
                category.append("RES")
                
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
        index_cat = 0
        for glosa in querys:
            tok = token(glosa)
            arrQuery = {} # [0]*len(bag_of_word)
            arrQueryFinal = ''
            l = 0
            for k in globalWords:
                for j in tok:
                    if k == j[0]:
                        arrQuery[l] = j[1]
                    else:
                        arrQuery[l] = 0
                l += 1

            matrix.append( arrQuery )

        k_min = 1
        k_max = 300
        # for i in range(1, 11):
        l = 0
        train = []
        test = []
        print str(k_min) + " -> " + str(k_max)
        for j in matrix:
            if l >= k_min and l <= k_max:
                train.append( (j, category[l] ) )
            test.append( (j) )
                
            l += 1
        k_min += 300
        k_max += 300
        
        print len(train)
        print len(test)
        #test_maxent(nltk.classify.MaxentClassifier.ALGORITHMS, train, test)
        #test_maxent( 'IIS', train, test )
        # sub_test = []
        # for i in range(0, 300):
        #     sub_test.append(category[i])

        tag_results = test_maxent( 'GIS', train, test )
        print 
        acurracy = 0.
        for i in range(0, len(tag_results)):
            # print str(category[i]) + " " + str(tag_results[i])
            if (category[i] == tag_results[i]):
                acurracy += 1

        print "Acurracy: " + str(acurracy/3000)
        print 

        inf_inf, nav_inf, res_inf = 0.0, 0.0, 0.0
        inf_nav, nav_nav, res_nav = 0.0, 0.0, 0.0
        inf_res, nav_res, res_res = 0.0, 0.0, 0.0

        for i in range(0, len(tag_results)):
            if category[i] == 'INF':
                if tag_results[i] == 'INF':
                    inf_inf += 1.
                elif tag_results[i] == 'NAV':
                    nav_inf += 1.
                elif tag_results[i] == 'RES':
                    res_inf += 1.
            
            elif category[i] == 'NAV':
                if tag_results[i] == 'INF':
                    inf_nav += 1.
                elif tag_results[i] == 'NAV':
                    nav_nav += 1.
                elif tag_results[i] == 'RES':
                    res_nav += 1.
            
            elif category[i] == 'RES':
                if tag_results[i] == 'INF':
                    inf_res += 1.
                elif tag_results[i] == 'NAV':
                    nav_res += 1.
                elif tag_results[i] == 'RES':
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
            #fof.close()
            #fom.close()
