import nltk, re
from collections import Counter
from numpy import linalg as LA
import numpy as np
import sys 

def token(files):
    data = files.lower()

    tokens = nltk.word_tokenize(data)
    nonPunct = re.compile('.*[\w+\W+].*')
    filtered = [w for w in tokens if nonPunct.match(w)]    
    counts = Counter(filtered)
    token = counts.items()

    return token #, len(counts)

"""def coseno(bigArray):
    bigArray_1 = np.array(bigArray)
    finalArray = np.zeros(shape=(30,30))

    for i in range(len(bigArray_1)):
        for j in range(len(bigArray_1)):
            finalArray[i][j] = "{0:.1f}".format( np.dot(bigArray_1[i], bigArray_1[j])/(LA.norm(bigArray_1[i], 2)*LA.norm(bigArray_1[j], 2)) )

    return finalArray, (finalArray.transpose() == finalArray).all()

def write(files, data):
    f = open (files, "w")
    f.write(str(data))
    f.close()"""

stop_words = [
    "a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"
]

if __name__=="__main__":
    #fo = open('renew_split-06-rodrigo-fuenzalida_tagged','a')
    try:
        arch = sys.argv[1]
        with open(arch) as fi:
            content = fi.readlines()
            sentence = ''
            wordsPocketINF = ''
            wordsPocketNAV = ''
            wordsPocketRES = ''
            countINF = 0
            countNAV = 0
            countRES = 0
            for i in content:
                data = i.split('\t')
                if data[0] == 'INF':
                    wordsPocketINF += data[1].split('\n')[0] + " "
                    countINF = countINF + 1
                elif data[0] == 'NAV':
                    wordsPocketNAV += data[1].split('\n')[0] + " "
                    countNAV = countNAV + 1
                elif data[0] == 'RES':
                    wordsPocketRES += data[1].split('\n')[0] + " "
                    countRES = countRES + 1

            tokINF = token(wordsPocketINF)
            tokNAV = token(wordsPocketNAV)
            tokRES = token(wordsPocketRES)

            finalTokINF = []
            for j in tokINF:
                try:
                    if stop_words.index(j[0]):
                        pass
                except:
                    finalTokINF.append(j[1])
            
            finalTokNAV = []
            for k in tokNAV:
                try:
                    if stop_words.index(j[0]):
                        pass
                except:
                    finalTokNAV.append(j[1])
            
            finalTokRES = []
            for l in tokRES:
                try:
                    if stop_words.index(j[0]):
                        pass
                except:
                    finalTokRES.append(j[1])
            
            globalVector = []
            for j in finalTokINF:
                globalVector.append(j)
            for k in finalTokNAV:
                globalVector.append(k)
            for l in finalTokRES:
                globalVector.append(l)
            
            finalVectorINF = []
            accountGlobal = float(len(globalVector))
            accountINF = float(len(finalTokINF))
            accountNAV = float(len(finalTokNAV))
            accountRES = float(len(finalTokRES))
            print "%d/%d = %.2f" % (accountGlobal, accountINF, accountGlobal/accountINF)
            print "%d/%d = %.2f" % (accountGlobal, accountNAV, accountGlobal/accountNAV)
            print "%d/%d = %.2f" % (accountGlobal, accountRES, accountGlobal/accountRES)
    except:
        print
        print "Modo de uso:"
        print "python tokens.py [nombre archivo]"
        print

    
        

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
