import nltk, re, sys 
from collections import Counter
from numpy import linalg as LA
import numpy as np
from math import sqrt, pow
from tabulate import tabulate

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
    tok = token(arrB)
    num, letterTok, letterTokFrec = [], [], []
    
    for i in tok:
        letterTok.append(i[0])
        letterTokFrec.append(i[1])
    
    k = 0
    for j in arrA.keys():
        if j in letterTok:
            num.append(letterTokFrec[k])
            k +=1
        else:
            num.append(0)
        
    k = 0
    for j in arrA.keys():
        suma += abs(arrA[j] - num[k])
        k += 1
    return suma

"""
#
# Calculo de distancia con 
# Algoritmo canberra
# 
"""
def canberra(arrA, arrB):
    suma = 0.0
    numerador = 0.0
    denominador = 0.0
    tok = token(arrB)
    num, letterTok, letterTokFrec = [], [], []

    for i in tok:
        letterTok.append(i[0])
        letterTokFrec.append(i[1])

    k = 0
    for j in arrA.keys():
        if j in letterTok:
            num.append(letterTokFrec[k])
            k +=1
        else:
            num.append(0)

    k = 0
    for j in arrA.keys():
        try:
            numerador = abs(arrA[j] - num[k])
            denominador = arrA[j] + num[k]
            suma += numerador/denominador
        except:
            suma += 0
        k += 1
    return suma
"""
#
# Calculo de distancia con 
# Algoritmo Squared Cord
# 
"""
def cord(arrA, arrB):
    suma = 0.0
    number = 0.0
    tok = token(arrB)
    num, letterTok, letterTokFrec = [], [], []

    for i in tok:
        letterTok.append(i[0])
        letterTokFrec.append(i[1])

    k = 0
    for j in arrA.keys():
        if j in letterTok:
            num.append(letterTokFrec[k])
            k +=1
        else:
            num.append(0)

    k = 0
    for j in arrA.keys():
        number = sqrt(arrA[j]) - sqrt(num[k])
        suma += pow(number, 2)
        k += 1
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
    num, letterTok, letterTokFrec = [], [], []

    for i in tok:
        letterTok.append(i[0])
        letterTokFrec.append(i[1])

    k = 0
    for j in arrA.keys():
        if j in letterTok:
            num.append(letterTokFrec[k])
            k +=1
        else:
            num.append(0)

    k = 0
    for j in arrA.keys():
        try:
            number = arrA[j] - num[k]
            numerador = pow(number, 2)
            denominador = arrA[j] + num[k]
            suma += numerador/denominador
        except:
            suma +=0
    return suma

def f_score(pres, recall, beta):
    numerador = pres*recall
    denominador = (pow(beta,2)*pres)+recall
    factor = 1+pow(beta, 2)
    try:
        return factor*(numerador/denominador)
    except:
        return 0

"""
 Funciones auxiliares
"""
def write(files, data):
    f = open (files, "w")
    f.write(data)
    f.close()

def min_val(val1, val2, val3):
    mini = min(val1, val2, val3)
    if mini == val1:
        lower = "INF"
    elif mini == val2:
        lower = "NAV"
    elif mini == val3:
        lower = "RES"

    return lower

"""
PARTE PRINCIPAL PROGRAMA
"""
if __name__=="__main__":
    try:
        if len(sys.argv) < 3:
            raise NameError('>>> Faltan Parametros.')
        else:
            arch = sys.argv[1]
            algo = sys.argv[2]
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

            arrayInf = [0] * len(bag_of_word)
            tempArrayInf = {}
            scalarInf = 1/countINF

            arrayNav = [0] * len(bag_of_word)
            scalarNav = 1/countNAV
            tempArrayNav = {}

            arrayRes = [0] * len(bag_of_word)
            scalarRes = 1/countRES
            tempArrayRes = {}
            
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
                                if str(k[0]) in tempArrayInf:
                                    tempArrayInf[str(k[0])] += k[1]
                                else:
                                    tempArrayInf[str(k[0])] = k[1]
                    except:
                        pass

                if data[0] == 'NAV':
                    try:
                        tokens = token(string)
                        for k in tokens:
                            pos = bag_of_word.index( k[0] )
                            if bag_of_word.index( k[0] ) >= 0:
                                arrayNav[pos] += k[1]
                                if str(k[0]) in tempArrayNav:
                                    tempArrayNav[str(k[0])] += k[1]
                                else:
                                    tempArrayNav[str(k[0])] = k[1]
                    except:
                        pass

                if data[0] == 'RES':
                    try:
                        tokens = token(string)
                        for k in tokens:
                            pos = bag_of_word.index( k[0] )
                            if bag_of_word.index( k[0] ) >= 0:
                                arrayRes[pos] += k[1]
                                if str(k[0]) in tempArrayRes:
                                    tempArrayRes[str(k[0])] += k[1]
                                else:
                                    tempArrayRes[str(k[0])] = k[1]
                    except:
                        pass

            totalInf = 0.0
            totalNav = 0.0
            totalRes = 0.0
            tempArrayInf = {}
            tempArrayNav = {}
            tempArrayRes = {}

            for data in globalWords.keys():
                string = data
                tempArrayInf[string] = arrayInf[bag_of_word.index( string )]*scalarInf
                tempArrayNav[string] = arrayNav[bag_of_word.index( string )]*scalarNav
                tempArrayRes[string] = arrayRes[bag_of_word.index( string )]*scalarRes

            if algo == "man":
                print "Manhattan: "
                inf, nav, res = [], [], []

                for query in querys:
                    inf.append(manhattan(tempArrayInf, query))
                    nav.append(manhattan(tempArrayNav, query))
                    res.append(manhattan(tempArrayRes, query))

            elif algo == "can":
                print "Canberra: "
                inf, nav, res = [], [], []

                for query in querys:
                    inf.append(canberra(tempArrayInf, query))
                    nav.append(canberra(tempArrayNav, query))
                    res.append(canberra(tempArrayRes, query))

            elif algo == "cor":
                print "Squared Cord: "
                inf, nav, res = [], [], []

                for query in querys:
                    inf.append(cord(tempArrayInf, query))
                    nav.append(cord(tempArrayNav, query))
                    res.append(cord(tempArrayRes, query))

            elif algo == "chi":
                print "Squared Chi-squared: "
                inf, nav, res = [], [], []

                for query in querys:
                    inf.append(chiSquared(tempArrayInf, query))
                    nav.append(chiSquared(tempArrayNav, query))
                    res.append(chiSquared(tempArrayRes, query))
                
            else:
                print "Opcion incorrecta"
                print
                print "Modo de uso:"
                print "python tokens.py [nombre archivo] [man|can|cor|chi]"
                print
            
            ######################################## FINAL DE LOS CALCULOS #############################################################

            accuracy = 0.0
            r_press_inf, p_press_inf, total_inf = 0.0, 0.0, 0.0
            r_press_nav, p_press_nav, total_nav = 0.0, 0.0, 0.0
            r_press_res, p_press_res, total_res = 0.0, 0.0, 0.0

            for i in range(0, len(inf)):
                cat = min_val(inf[i] , nav[i] , res[i])
                if cat == category[i]:
                    accuracy += 1.0
                #print "%.2f | %.2f | %.2f | %s | %s " % (inf[i] , nav[i] , res[i], min_val(inf[i] , nav[i] , res[i]), category[i])
                
                if cat == "INF" and category[i] == "INF": # precision
                    p_press_inf += 1.0
                elif cat == "NAV" and category[i] == "NAV":
                    p_press_nav += 1.0
                elif cat == "RES" and category[i] == "RES":
                    p_press_res += 1.0
                
                if cat == "INF": # recall
                    r_press_inf += 1.0
                elif cat == "NAV":
                    r_press_nav += 1.0
                elif cat == "RES":
                    r_press_res += 1.0

                if category[i] == "INF": # total
                    total_inf += 1.0
                elif category[i] == "NAV":
                    total_nav += 1.0
                elif category[i] == "RES":
                    total_res += 1.0

            # print str(total_inf) + " | " + str(total_nav) + " | " + str(total_res)
            # print str(p_press_inf) + " | " + str(p_press_nav) + " | " + str(p_press_res)
            # print str(r_press_inf) + " | " + str(r_press_nav) + " | " + str(r_press_res)
            print "Accuracy: {0:.2f}".format(accuracy/3000)
            print

            press_inf = p_press_inf/total_inf
            recall_inf = r_press_inf/total_inf
            
            press_nav = p_press_nav/total_nav
            recall_nav = r_press_nav/total_nav
            
            press_res = p_press_res/total_res
            recall_res = r_press_res/total_res
            
            headers = ["Categoria", "Precision", "Recall", "F-Score"]
            table = [
                ["INF", "{0:.2f}".format(press_inf), "{0:.2f}".format(recall_inf), f_score(press_inf, recall_inf, 1) ],
                ["NAV", "{0:.2f}".format(press_nav), "{0:.2f}".format(recall_nav), "{0:.2f}".format(f_score(press_nav, recall_nav, 1)) ],
                ["RES", "{0:.2f}".format(press_res), "{0:.2f}".format(recall_res), "{0:.2f}".format(f_score(press_res, recall_res, 1)) ]
            ]
            print tabulate(table, headers, tablefmt="orgtbl")
            print
                   
    except Exception, e:
        print str(e)
        print
        print "Modo de uso:"
        print "python tokens.py [nombre archivo] [man|can|cor|chi]"
        print
    finally:
        fi.close()
    
#pasar vector de consulta no global
#accuracy function

#3000  
#   dinf dnav dres auraccy manual
# 1                   inf    inf
# 2
# 3
# .
# .
# .
# .
# 3000
# diferencia entre metrica de distancia y metrica de similitud.
# 
# 
# 