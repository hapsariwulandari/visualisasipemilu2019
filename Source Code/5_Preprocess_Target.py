import os
import csv
import gensim
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer
import string
from gensim import corpora
from pprint import pprint
import Sastrawi
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

nltk.download('punkt')
nltk.download('stopwords')

from nltk.corpus import stopwords

#os.chdir("D:/0 SEM 8 3-20-20/TA/Bimbingan 3")

en_stops = set(stopwords.words('english'))

with open('hasil_untuk_preprocess.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    f=open("hasilprocessingtarget.csv", "a+")
    
    for row in reader:
        alltarget = row['target']
        #print(allmotivasi)

        #Casefolding
        mot_casefold = alltarget.casefold()
        #print(mot_casefold)

        #Tokenization
        token_casefold = nltk.word_tokenize(mot_casefold)
        tokenizer = RegexpTokenizer(r'\w+')
        mot_token = tokenizer.tokenize(str(token_casefold))
        #print (mot_token)

        #Stopwords
        in_stops = set(stopwords.words('indonesian'))
        mot_word = []
        for word in mot_token:
            if word not in in_stops:
                mot_word.append(word)
        #print(mot_word)

        #Stemming
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        mot_stem = []
        for i in range(0, len(mot_word)):
            mot_stem.append(stemmer.stem(mot_word[i]))
        print(mot_stem)
        listtarget = [ k for k in mot_stem ]
            
        f.write(str(mot_stem)+ "\r\n")
        f.flush()

    f.close()
 



        
