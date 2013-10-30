import nltk.classify.util
from nltk.classify import MaxentClassifier
from nltk.corpus import movie_reviews
import nltk, re, sys 
from collections import Counter
import numpy as np
from math import sqrt, pow
from tabulate import tabulate
from numpy.random import rand


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
"""
#
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
            category.append(1)
        elif data[0] == "NAV":
            category.append(2)
        elif data[0] == "RES":
            category.append(3)
            
        querys.append(data[1].rstrip())
        tok = token(data[1].rstrip())
        query = []
        
        for j in tok:
            if str(j[0]) in globalWords:
                globalWords[str(j[0])] += j[1]
            else:
                globalWords[str(j[0])] = j[1]

print globalWords"""
# Classifier tester

import numpy;
import scipy;
import nltk;

print 'NumPy Version: ', numpy.__version__
print 'SciPy Version: ', scipy.__version__
print 'NLTK Version: ', nltk.__version__

print nltk.usage(nltk.ClassifierI)

# Training & test data
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
        category.append(1)
    elif data[0] == "NAV":
        category.append(2)
    elif data[0] == "RES":
        category.append(3)
        
    querys.append(data[1].rstrip())
    tok = token(data[1].rstrip())
    query = []
    
    for j in tok:
        if str(j[0]) in globalWords:
            globalWords[str(j[0])] += j[1]
        else:
            globalWords[str(j[0])] = j[1]

train = []
for i in range(1, 11):
    fof = open("train/train_"+str(i)+".txt", 'r')
    content = fof.readlines()
    dictio = {}
    for line in content:
        data = line.split(" ")
        etiq = data.pop(0)
        for j in data:
            pos = j.replace("\r", "").replace("\n", "").split(":")
            
    fof.close()
"""train = [
     (dict(a=1,b=1,c=1), 'y'),
     (dict(a=1,b=1,c=1), 'x'),
     (dict(a=1,b=1,c=0), 'y'),
     (dict(a=0,b=1,c=1), 'x'),
     (dict(a=0,b=1,c=1), 'y'),
     (dict(a=0,b=0,c=1), 'y'),
     (dict(a=0,b=1,c=0), 'x'),
     (dict(a=0,b=0,c=0), 'x'),
     (dict(a=0,b=1,c=1), 'y')
     ]
test = [
     (dict(a=1,b=0,c=1)), # unseen
     (dict(a=1,b=0,c=0)), # unseen
     (dict(a=0,b=1,c=1)), # seen 3 times, labels=y,y,x
     (dict(a=0,b=1,c=0)) # seen 1 time, label=x
     ]

def test_maxent(algorithms):
    classifiers = {}
    for algorithm in nltk.classify.MaxentClassifier.ALGORITHMS:
        if algorithm == 'MEGAM'  or  algorithm=='TADM':
            print '(skipping %s)' % algorithm
        else:
            try:
                classifiers[algorithm] = nltk.MaxentClassifier.train(
                    train, algorithm, trace=0, max_iter=1000)
            except Exception, e:
                classifiers[algorithm] = e
    print ' '*11+''.join(['      test[%s]  ' % i
                          for i in range(len(test))])
    print ' '*11+'     p(x)  p(y)'*len(test)
    print '-'*(11+15*len(test))
    for algorithm, classifier in classifiers.items():
        print '%11s' % algorithm,
        if isinstance(classifier, Exception):
            print 'Error: %r' % classifier; continue
        for featureset in test:
            pdist = classifier.prob_classify(featureset)
            print '%8.2f%6.2f' % (pdist.prob('x'), pdist.prob('y')),
        print

#test_maxent(nltk.classify.MaxentClassifier.ALGORITHMS)
test_maxent( ['lbfsgb'] )"""