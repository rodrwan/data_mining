import numpy as np

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler


##############################################################################
# Generate sample data
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
        raise NameError('>>> Faltan Parametros.')
    else:
        arch = sys.argv[1]
        eps = int(sys.argv[2])
        minPts = int(sys.argv[3])
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
        
        X = np.array(matrix)
        ##############################################################################
        # Compute DBSCAN
        for e in range(0, eps):
            for m in range(0, minPts):
                #print "Eps: " + str(e+1)
                #print "minPts: " + str(m+1)
                db = DBSCAN(eps=(e+1), min_samples=(m+1)).fit(X)
                core_samples = db.core_sample_indices_
                labels = db.labels_
                
                inf = 0.
                nav = 0.
                res = 0.
                noise = 0.
                categoryArray = []
                for i in labels:
                    if i == -1:
                        categoryArray.append('INF')
                        inf += 1.
                    elif i == 0:
                        categoryArray.append('NAV')
                        nav += 1.
                    elif i == 1:
                        categoryArray.append('RES')
                        res += 1.
                    else:
                        categoryArray.append('NOISE')
                        noise += 1.
                print

                j = 0
                accuracy = 0.
                accuracyInf = 0.
                accuracyNav = 0.
                accuracyRes = 0.
                accuracyNoise = 0.

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
                        else:
                            accuracyNoise += 1.
                    j += 1

                headers = ["Eps", "MinPts", "NOISE"] #
                table = [
                    [
                        (e+1),
                        (m+1),
                        noise,
                    ],
                ]
                print tabulate(table, headers, tablefmt="orgtbl")
                #print
                #print "Accuracy: {0:.2f}".format(accuracy/3000)
                #print
                #print "####################################################################"
                #print

