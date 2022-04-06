from hashlib import new
import imp
from operator import index
import random
from tkinter import Label
import numpy as np
from nltk.corpus import wordnet 
import nltk
import random
from random import shuffle
from collections import Counter, defaultdict
from zmq import TYPE
from scheme import *
from typing import Callable, Dict, List, Type
import re
import more_itertools
stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 
			'ours', 'ourselves', 'you', 'your', 'yours', 
			'yourself', 'yourselves', 'he', 'him', 'his', 
			'himself', 'she', 'her', 'hers', 'herself', 
			'it', 'its', 'itself', 'they', 'them', 'their', 
			'theirs', 'themselves', 'what', 'which', 'who', 
			'whom', 'this', 'that', 'these', 'those', 'am', 
			'is', 'are', 'was', 'were', 'be', 'been', 'being', 
			'have', 'has', 'had', 'having', 'do', 'does', 'did',
			'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or',
			'because', 'as', 'until', 'while', 'of', 'at', 
			'by', 'for', 'with', 'about', 'against', 'between',
			'into', 'through', 'during', 'before', 'after', 
			'above', 'below', 'to', 'from', 'up', 'down', 'in',
			'out', 'on', 'off', 'over', 'under', 'again', 
			'further', 'then', 'once', 'here', 'there', 'when', 
			'where', 'why', 'how', 'all', 'any', 'both', 'each', 
			'few', 'more', 'most', 'other', 'some', 'such', 'no', 
			'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 
			'very', 's', 't', 'can', 'will', 'just', 'don', 
			'should', 'now', '']
########################################################################
# Synonym replacement
# Replace n words in the sentence with synonyms from wordnet
#input: ['She','did','not','complain','of','headache','or','any','other','neurological','symptoms','.']
#       ['O','O','O','O','O','B-problem','O','B-problem','I-problem','I-problem','I-problem','O']
########################################################################

# class SR():
#     def __init__(self, ne_words:List[str],ne_labels:List[str],scheme:str):
#         self.dic = defaultdict(list)
#         self.words=ne_words
#         self.label=ne_labels
#         self.scheme = scheme
    
#     def sr(words,label,n):
#         new_words = words.copy()
#         random_word_list = list(set([word for word in words if word not in stop_words]))
#         new_labels=labels.copy()
#         random.shuffle(random_word_list)
#         num_replaced = 0
#         for random_word in random_word_list:
#             synonyms = get_synonyms(random_word)
#             if len(synonyms) >= 1:
#                 synonym = random.choice(list(synonyms))
#                 new_words = [synonym if word == random_word else word for word in new_words]
# 			    #print("replaced", random_word, "with", synonym)
#                 num_replaced += 1
#                 if num_replaced >= n: #only replace up to n words
#                     break

#                 sentence = ' '.join(new_words)
#                 new_words = sentence.split(' ')
            
#         return new_words

def synonym_replacement(words,labels,n):
    origin_type='O'
    tagger = create_tagger('IOB2')
    new_words = words.copy()
    random_word_list = list(set([word for word in words if word not in stop_words]))
    new_labels=labels.copy()
    random.shuffle(random_word_list)
    num_replaced = 0
    for random_word in random_word_list:
        synonyms = get_synonyms(random_word)
        if len(synonyms) >= 1:
            synonym = random.choice(list(synonyms))
            new_words = [synonym if word == random_word else word for word in new_words]
            label=re.match(r'(.*)-(.*)',labels[words.index(random_word)])
            if(label==None):
                label_type='O'
            else:
                label_type=label.group(2)
                origin_type=label.group(1) 
            for i in find_index(words,random_word):
                new_labels[i]=tagger.tag(synonym.split(' '),label_type,origin_type)
            # print("replaced", random_word, "with", synonym)
            # print("original_label_index", words.index(random_word),"original_label",labels[words.index(random_word)],'type',label_type)
            # print("original_label",labels[words.index(random_word)],'new_label',tagger.tag(synonym.split(' '),label_type,origin_type))
            num_replaced += 1
            if num_replaced >= n: #only replace up to n words
                break

	#this is stupid but we need it, trust me
    sentence = ' '.join(new_words)
    new_words = sentence.split(' ')
    new_labels=list(more_itertools.collapse(new_labels))
    return new_words,new_labels

def get_synonyms(word):
	synonyms = set()
	for syn in wordnet.synsets(word): 
		for l in syn.lemmas(): 
			synonym = l.name().replace("_", " ").replace("-", " ").lower()
			synonym = "".join([char for char in synonym if char in ' qwertyuiopasdfghjklzxcvbnm'])
			synonyms.add(synonym) 
	if word in synonyms:
		synonyms.remove(word)
	return list(synonyms)

def find_index(src_list, target):
    """在给定集合中寻找目标所在索引"""

    #用来存储目标索引的列表
    dst_index_list = []

    #在给定集合中挨个比对，若与目标匹配，保留索引
    for index in range(len(src_list)):
        if (src_list[index] == target):
            dst_index_list.append(index)

    #返回目标索引列表
    return dst_index_list

if __name__ == '__main__':
    words=['She','did','not','complain','of','headache','or','any','other','neurological','symptoms','.']
    labels=['O','O','O','O','O','B-problem','O','B-problem','I-problem','I-problem','I-problem','O']

    # words=['Torsade','de','pointes','ventricular','tachycardia','during','low','dose','intermittent','dobutamine','treatment','in','a','patient','with','dilated','cardiomyopathy','and','congestive','heart','failure','.']
    # labels=['O','O','O','O','O','O','O','O','O','B-Chemical','O','O','O','O','O','O','O','O','O','O','O','O']

    new_words,new_labels=synonym_replacement(words=words,labels=labels,n=len(words)/3)

    print(new_words,new_labels)



