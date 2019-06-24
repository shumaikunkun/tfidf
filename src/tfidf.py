import pandas as pd
from janome.tokenizer import Tokenizer
import re
import math

query = '吾輩は猫である'
query_words=[token.surface for token in Tokenizer().tokenize(query) if not re.fullmatch(r"[あ-ん]|、|。|　",token.surface)]
query_file = 'query'

arr=[line.strip().split("\t") for line in open('../index/index2.txt', 'r')]

idf_scores={a[0]:float(a[3]) for a in arr}
tfidf_scores={w:{} for w in idf_scores}
for a in arr: tfidf_scores[a[0]][a[1]]=float(a[4])
tfidf_table = pd.DataFrame(tfidf_scores).fillna(0)

query_tf={w:0 for w in idf_scores}
for w in query_tf:
    for q in query_words:
        if w==q: query_tf[w]+=1
query_tfidf={w:{query_file:query_tf[w]*idf_scores[w]} for w in idf_scores}
query_table=pd.DataFrame(query_tfidf)

ranking_docs={a[1]:1 for q in query_words for a in arr if a[0]==q}
query_vec=query_table.loc[query_file]

for file in ranking_docs:
    doc_vec = tfidf_table.loc[file]
    numerator = query_value = doc_value =  0
    for i in range(len(query_vec.values)):
        numerator += query_vec.values[i] * doc_vec.values[i]
        query_value += query_vec.values[i] ** 2
        doc_value += doc_vec.values[i] ** 2
    denominator = math.sqrt(query_value) * math.sqrt(doc_value)
    ranking_docs[file] = numerator / denominator
sorted(ranking_docs.items(), key=lambda x:-x[1])
