"""
http://stackoverflow.com/questions/4131982/count-the-number-of-elements-of-same-value-in-python
http://stackoverflow.com/questions/2600191/how-to-count-the-occurrences-of-a-list-item-in-python
# 
#  Muchas dudas
#  pregunta 1 aun no resuelta
#  pregunta 2 muuuuy lejos de ser resuelta
#  pregunta 3
#  pregunta 4
#  pregunta 5
#  pregunta 6
#  pregunta 7
# 

"""
import nltk, re
from collections import Counter
from numpy import linalg as LA
import numpy as np
import matplotlib.pyplot as plt
import sys 
from math import sqrt, pow

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
# Calculo de distancia con 
# Algoritmo de manhattan
# 
"""
def manhattan(arrA, arrB):
    suma = 0.0
    for i in range(0, len(arrA)):
        suma += abs(arrA[i] - arrB[i])
    return sqrt(suma)
"""
#
# Calculo de distancia con 
# Algoritmo camberra
# 
"""
def canberra(arrA, arrB):
    suma = 0.0
    numerador = 0.0
    denominador = 0.0
    for i in range(0, len(arrA)):
        numerador = abs(arrA[i] - arrB[i])
        denominador = arrA[i] + arrB[i]
        suma += numerador/denominador
    return suma

"""
#
# Calculo de distancia con 
# Algoritmo Squared Cord
# 
"""
def card(arrA, arrB):
    suma = 0.0
    number = 0.0
    for i in range(0, len(arrA)):
        number = sqrt(arrA[i]) - sqrt(arrB[i])
        suma += pow(number, 2)
    return suma

"""
#
# Calculo de distancia con 
# Algoritmo Squared Chi-squered
# 
"""
def chiSquared(arrA, arrB):
    suma = 0.0
    numerador = 0.0
    denominador = 0.0
    number = 0.0
    for i in range(0, len(arrA)):
        number = arrA[i] - arrB[i]
        numerador = pow(number, 2)
        denominador = arrA[i] + arrB[i]
        suma += numerador/denominador
    return suma

"""def coseno(bigArray):
    bigArray_1 = np.array(bigArray)
    finalArray = np.zeros(shape=(30,30))

    for i in range(len(bigArray_1)):
        for j in range(len(bigArray_1)):
            finalArray[i][j] = "{0:.1f}".format( np.dot(bigArray_1[i], bigArray_1[j])/(LA.norm(bigArray_1[i], 2)*LA.norm(bigArray_1[j], 2)) )

    return finalArray, (finalArray.transpose() == finalArray).all()
"""

def write(files, data):
    f = open (files, "w")
    f.write(data)
    f.close()



if __name__=="__main__":
    #fo = open('renew_split-06-rodrigo-fuenzalida_tagged','a')
    try:
        arch = sys.argv[1]
        fi =  open(arch, 'r')
        content = fi.readlines()
        globalWords = {}
        countINF = 0.0
        countNAV = 0.0
        countRES = 0.0
        for i in content:
            data = i.split('\t')
            if data[0] == 'INF':
                countINF += 1
            elif data[0] == 'NAV':
                countNAV += 1
            elif data[0] == 'RES':
                countRES += 1

            for j in token(data[1].split('\n')[0].rstrip()):
                if str(j[0]) in globalWords:
                    globalWords[str(j[0])] += j[1]
                else:
                    globalWords[str(j[0])] = j[1]

        bag_of_word = []
        bag_of_word_num = []
        bag_of_word_count = 0
        for word in globalWords.keys():
            bag_of_word.append(word)
            bag_of_word_count += globalWords[word]
            bag_of_word_num.append(globalWords[word])

        arrayInf = [0] * len(bag_of_word)
        scalarInf = 1/countINF
        arrayNav = [0] * len(bag_of_word)
        scalarNav = 1/countNAV
        arrayRes = [0] * len(bag_of_word)
        scalarRes = 1/countRES


        for i in content:
            data = i.split('\t')
            string = data[1].split('\n')[0].rstrip()
            
            if data[0] == 'INF':
                try:
                    tokens = token(string)
                    for k in tokens:
                        pos = bag_of_word.index( k[0] )
                        if bag_of_word.index( k[0] ) >= 0:
                            arrayInf[pos] += k[1]
                except:
                    pass

            elif data[0] == 'NAV':
                try:
                    tokens = token(string)
                    for k in tokens:
                        pos = bag_of_word.index( k[0] )
                        if bag_of_word.index( k[0] ) >= 0:
                            arrayNav[pos] += k[1]
                except:
                    pass

            elif data[0] == 'RES':
                try:
                    tokens = token(string)
                    for k in tokens:
                        pos = bag_of_word.index( k[0] )
                        if bag_of_word.index( k[0] ) >= 0:
                            arrayRes[pos] += k[1]
                except:
                    pass
        
        totalInf = 0.0
        totalNav = 0.0
        totalRes = 0.0
        for data in globalWords.keys():
            string = data
            totalInf += arrayInf[bag_of_word.index( string )]*scalarInf
            totalNav += arrayNav[bag_of_word.index( string )]*scalarNav
            totalRes += arrayRes[bag_of_word.index( string )]*scalarRes

        print totalInf
        print totalNav
        print totalRes
        print 
        print "INF"
        print "Manhattan: " + str(manhattan(arrayInf, bag_of_word_num))
        print "Canberra: " + str(canberra(arrayInf, bag_of_word_num))
        print "Squared Cord: " + str(card(arrayInf, bag_of_word_num))
        print "Squared Chi-Squered: " + str(chiSquared(arrayInf, bag_of_word_num))
        print
        print "NAV"
        print "Manhattan: " + str(manhattan(arrayNav, bag_of_word_num))
        print "Canberra: " + str(canberra(arrayNav, bag_of_word_num))
        print "Squared Cord: " + str(card(arrayNav, bag_of_word_num))
        print "Squared Chi-Squered: " + str(chiSquared(arrayNav, bag_of_word_num))
        print
        print "RES"
        print "Manhattan: " + str(manhattan(arrayRes, bag_of_word_num))
        print "Canberra: " + str(canberra(arrayRes, bag_of_word_num))
        print "Squared Cord: " + str(card(arrayRes, bag_of_word_num))
        print "Squared Chi-Squered: " + str(chiSquared(arrayRes, bag_of_word_num))
        print
        # for data in globalWords.keys():
        #     try:
        #         string = data
        #         total = arrayInf[bag_of_word.index( string )]+arrayNav[bag_of_word.index( string )]+arrayRes[bag_of_word.index( string )]
                
        #         if total == globalWords[data]:
        #             print bag_of_word[bag_of_word.index( string )] + " -> " + str( total ) + " => " + str(data[1]) + " Exito"

        #         else:
        #             print "==================================================================="
        #             print "fallo en => " + string
        #             print bag_of_word[bag_of_word.index( string )] + " -> " \
        #             + str(arrayInf[bag_of_word.index( string )]) + "  " \
        #             + str(arrayNav[bag_of_word.index( string )]) + "  " \
        #             + str(arrayRes[bag_of_word.index( string )]) + " = " \
        #             + str( total ) + " => " + str(data[1])
        #             print "==================================================================="

        #     except:
        #         pass
        
        
        # finalVectorINF = []

        # accountGlobal = float(len(globalVector))
        # print globalVectorINFNum
        # print "%d/%d = %.2f" % (accountGlobal, countINF, accountGlobal/countINF)
        plt.plot(arrayInf)
        plt.ylabel('some numbers')
        plt.show()

        # print globalVectorNAVNum
        # print "%d/%d = %.2f" % (accountGlobal, countNAV, accountGlobal/countNAV)
        plt.plot(arrayNav)
        plt.ylabel('some numbers')
        plt.show()
        
        # print globalVectorRESNum
        # print "%d/%d = %.2f" % (accountGlobal, countRES, accountGlobal/countRES)
        plt.plot(arrayRes)
        plt.ylabel('some numbers')
        plt.show()
        # """
    except:
        print
        print "Modo de uso:"
        print "python tokens.py [nombre archivo]"
        print
    finally:
        fi.close()
    
        

        #print globalVector

        # x = np.array(general_vector)
        # vector_mag = np.linalg.norm(x)
        # vector_centroide_inf = []
        # vector_centroide_nav = []
        # vector_centroide_res = []
        # for j in general_vector:
        #     vector_centroide_inf.append(float(j/countINF))

        # for j in general_vector:
        #     vector_centroide_nav.append(float(j/countNAV))
        
        # for j in general_vector:
        #     vector_centroide_res.append(float(j/countRES))
        
        # print vector_centroide_inf

        #x = np.array([1,2,3,4,5])
        #np.linalg.norm(x)

        # for i in content:
        #     general_vector = []
        #     data =  i.split('\t')
        #     tok = token(data[1])
        #     for j in  tok:
        #         general_vector.append(j[1])
        #     fo.write(data[0] + "\t" + data[1].split('\n')[0] + "\t" + str(general_vector) + "\n")
