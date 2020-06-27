import os, re, csv
from pprint import pprint
from nltk.tokenize import RegexpTokenizer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from gensim.models import Phrases
from gensim.corpora import Dictionary
from gensim.models import AuthorTopicModel
from pprint import pprint
import collections
import pandas as pd
from gensim.models.coherencemodel import CoherenceModel

#os.chdir("D:/0 SEM 8 3-20-20/TA/Bimbingan 4")

def topik():
	docs=[]
	doc_ids=[]
	i=0
	tokenizer = RegexpTokenizer(r'\w+')
	with open('atm_motivasi.csv') as raw:
	    reader = csv.reader(raw)
	    for row in reader:
	        gabung = ''.join(row[1])
	        token = tokenizer.tokenize(gabung)
	        doc_id = row[0]
	        if len(token)>4:
	            docs.append(token)
	            doc_ids.append(doc_id)
	            i=i+1

	author2doc = dict() 
	i = 0
	with open('partai_csv.csv', errors='ignore',encoding="utf8") as author:
	    readCSV = csv.reader(author, delimiter=';')
	    next(readCSV, None)
	    for contents in readCSV:
	        authorname = contents[1]
	        authorname = re.sub('\s', ' ', authorname)
	        ids = contents[0]
	        if not author2doc.get(authorname):
	            author2doc[authorname] = []
	        author2doc[authorname].append(ids)

	doc_id_dict = dict(zip(doc_ids, range(len(doc_ids))))

	for a, a_doc_ids in author2doc.items():
	    for i, doc_id in enumerate(a_doc_ids):
	        author2doc[a][i] = doc_id_dict[doc_id]

	dictionary = Dictionary(docs)
	# Remove rare and common tokens.
	# Filter out words that occur too frequently or too rarely.
	max_freq = 0.9
	min_wordcount = 30
	dictionary.filter_extremes(no_below=min_wordcount, no_above=max_freq)

	_ = dictionary[0]

	corpus = [dictionary.doc2bow(doc) for doc in docs]
	
	print('Number of authors: %d' % len(author2doc))
	print('Number of unique tokens: %d' % len(dictionary))
	print('Number of documents: %d' % len(corpus))
	print('Dictionary sudah terbentuk')

	val = input("Jumlah topik: ")
	jmltopik = int(val)

	import logging
	logger = logging.getLogger()
	fhandler = logging.FileHandler(filename='atmmotivasi-' + str(jmltopik) + '-logging.csv', mode='w')
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	fhandler.setFormatter(formatter)
	logger.addHandler(fhandler)
	logger.setLevel(logging.DEBUG)

	atm1 = AuthorTopicModel(corpus=corpus, 
                        author2doc=author2doc,
                        num_topics=jmltopik,
                        id2word=dictionary.id2token, 
                        alpha = 'auto',
                        passes=1000,
                        eval_every=10,
                        iterations=10000)

	model1 = atm1.show_topics(num_topics=jmltopik, num_words = 15, formatted=False)
	
	cm1 = CoherenceModel(model=atm1,
	                    corpus=corpus, 
	                    dictionary=dictionary,
	                    texts=docs,
	                    coherence='c_v')

	coherence = cm1.get_coherence()

	topics = pd.Series((v for v in model1), name='topic')
	coherence = pd.Series(coherence, name='coherence')

	df_banyak = pd.concat([topics, coherence], axis=1)
	df_banyak.to_csv('atmmotivasi-' + str(jmltopik) + '-coherence.csv', index=False)

	topic_labels = ['0','1','2','3','4','5','6','7','8','9','10']

	top_topics = atm1.top_topics(atm1.corpus, topn=20)
	author_vecs = [atm1.get_author_topics(author) for author in atm1.id2author.values()]
	atm1.save('atmmotivasi-' + str(jmltopik) + '-topik.atmodel')

	with open('atmmotivasi-' + str(jmltopik) + '-topik-jumlahkata.csv','w') as tulisFile:
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

	with open('atmmotivasi-' + str(jmltopik) + '-topik-detail.csv','w') as tulisFile:
	    tulisFileWriter = csv.writer(tulisFile,lineterminator='\n')
	    d=0
	    for items in top_topics:
	        v=0
	        for items in top_topics[0][0]:
	            h = top_topics[d][0][v][0]
	            w = top_topics[d][0][v][1]
	            v=v+1
	            tulisFileWriter.writerow([d,h,w])
	            if v ==10:
	                break
	        d=d+1
	tulisFile.close()
	print('detail topik udah')

	with open('atmmotivasi-' + str(jmltopik) + 'probabilitas.csv','w') as tulisFile:
	    tulisFileWriter = csv.writer(tulisFile,lineterminator='\n')
	    initopik = 0
	    i=0
	    for keys in author2doc:
	        cobaauthor = author_vecs[i][0][0]
	        cobatopik  = author_vecs[i][0][1]
	        if len(author_vecs[i])>1:
	            d=0
	            for items in author_vecs[i]:
	                cobaauthor2 = author_vecs[i][d][0]
	                cobatopik2  = author_vecs[i][d][1]
	                tulisFileWriter.writerow([keys,cobatopik2,cobaauthor2])
	                d=d+1
	        else:
	            tulisFileWriter.writerow([keys,cobatopik,cobaauthor])
	        i=i+1
	    tulisFile.close()

	lines = [line.strip() for line in open('atmmotivasi-' + str(jmltopik) + '-logging.csv')]

	for x in lines:
	    try:
	        found = re.search('per-word bound, (.+?) perplexity', x).group(1)
	        f = open('atmmotivasi-' + str(jmltopik) + '-perplexity.csv', 'a+')
	        f.write("\n"+found)
	    except AttributeError:
	        found = 'tidak ada' # apply your error handling
	print('perplexity udah')

if __name__ == '__main__':
	topik()