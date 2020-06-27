import os, re, csv
from pprint import pprint
from nltk.tokenize import RegexpTokenizer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from gensim.models import Phrases
from gensim.corpora import Dictionary
from gensim.models.ldamodel import LdaModel
from pprint import pprint
import collections
import pandas as pd
from gensim.models.coherencemodel import CoherenceModel

#os.chdir("D:/0 SEM 8 3-20-20/TA/Bimbingan 4")

def lda():
	docs=[]
	i=0
	tokenizer = RegexpTokenizer(r'\w+')
	with open("D:/0 SEM 8 3-20-20/TA/Bimbingan 4/lda_target.csv") as raw:
	    reader = csv.reader(raw)
	    for row in reader:
	        gabung = ''.join(row[0])
	        token = tokenizer.tokenize(gabung)
	        if len(token)>2:
	            docs.append(token)
	            i=i+1

	dictionary = Dictionary(docs)
	max_freq = 0.9
	min_wordcount = 25
	dictionary.filter_extremes(no_below=min_wordcount, 
    no_above=max_freq)

	_ = dictionary[0]

	corpus = [dictionary.doc2bow(doc) for doc in docs]

	print('Number of unique tokens: %d' % len(dictionary))
	print('Number of documents: %d' % len(corpus))
	print('Dictionary sudah terbentuk')

	val = input("Jumlah topik: ")
	jmltopik = int(val)

	import logging
	logger = logging.getLogger()
	fhandler = logging.FileHandler(filename='ldatarget-logging-' + 
    str(jmltopik) + '.csv', mode='w')
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s 
    - %(message)s')
	fhandler.setFormatter(formatter)
	logger.addHandler(fhandler)
	logger.setLevel(logging.DEBUG)

	lda1 = LdaModel(corpus=corpus, 
                    num_topics=jmltopik,
                    id2word=dictionary.id2token,
                    alpha = 'auto',
                    eta='auto',
                    passes=1000,
                    eval_every=10,
                    iterations=10000)

	top_topics = lda1.show_topics(num_topics=jmltopik, num_words = 15, formatted=False)
	detail = pd.DataFrame(top_topics)
	detail.to_csv('ldatarget-' + str(jmltopik) + 'topik-detail.csv', index=False)
	print("detail topik udah")

	cm1 = CoherenceModel(model=lda1,
	                    corpus=corpus, 
	                    dictionary=dictionary,
	                    texts=docs,
	                    coherence='c_v')

	coherence = cm1.get_coherence()

	topics = pd.Series((v for v in top_topics), name='topic')
	coherence = pd.Series(coherence, name='coherence')

	df_banyak = pd.concat([topics, coherence], axis=1)
	df_banyak.to_csv('ldatarget-coh-' + str(jmltopik) + '.csv', index=False)

	topic_labels = ['0','1','2','3','4','5','6','7','8','9','10','11','12']

	lda1.save('ldatarget-' + str(jmltopik) + 'topik.ldamodel')

	with open('ldatarget-' + str(jmltopik) + 'topik-jumlahkata.csv','w') as tulisFile:
	    tulisFileWriter = csv.writer(tulisFile,lineterminator='\n')
	    hasil=[]
	    i=0
	    for items in docs:
	        b=0
	        for items in docs[i]:
	            hasil.append(docs[i][b])
	            tulisFileWriter.writerow([docs[i][b]])
	            b=b+1
	        i=i+1
	tulisFile.close()
	print('jumlah kata sudah')

	# with open('lda+kubu' + kubu + '-' + str(jmltopik) + 'topik-detail.csv','w') as tulisFile:
	#     tulisFileWriter = csv.writer(tulisFile,lineterminator='\n')
	#     d=0
	#     for items in top_topics:
	#         v=0
	#         for items in top_topics[d][]:
	#             h = top_topics[d][0][v][0]
	#             w = top_topics[d][0][v][1]
	#             v=v+1
	#             tulisFileWriter.writerow([d,h,w])
	#             if v ==10:
	#                 break
	#         d=d+1
	# tulisFile.close()
	# print('detail topik udah')

	lines = [line.strip() for line in open('ldatarget-logging-' + str(jmltopik) + '.csv')]

	for x in lines:
	    try:
	        found = re.search('per-word bound, (.+?) perplexity', x).group(1)
	        f = open('ldatarget-' + str(jmltopik) + 'topik-perplexity.csv', 'a+')
	        f.write("\n"+found)
	    except AttributeError:
	        found = 'not found' # apply your error handling
	print('perplexity done')

if __name__ == '__main__':
	lda()