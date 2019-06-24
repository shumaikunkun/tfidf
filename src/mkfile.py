import os
from janome.tokenizer import Tokenizer
import re
import math
f = open("../index/index3.txt", 'w')
dict={}

for filename in os.listdir("../data"):
    for line in open("../data/"+filename, 'r', encoding='utf-8'):
        for token in Tokenizer().tokenize(line):
            if not re.fullmatch(r"[あ-ん]|、|。",token.surface):
                if token.surface in dict:
                    if filename in dict[token.surface]: dict[token.surface][filename]+=1
                    else: dict[token.surface][filename]=1
                else: dict[token.surface]={filename:1}

for key1 in sorted(dict):
    for key2 in sorted(dict[key1]):
        tf=dict[key1][key2]
        idf=math.log(10/len(dict[key1])+1)
        f.write(key1 + '\t' + key2 + '\t' + str(tf) + '\t' + str(idf) + '\t' + str(tf*idf) + '\n')

f.close()
