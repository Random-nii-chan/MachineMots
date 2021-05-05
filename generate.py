# -*- coding: utf-8 -*-
"""
Generates word from trigramm transition matrix stored in a binary file
Checks whether the word already exists
"""

import os
import argparse
import codecs
import numpy as np
from numpy.random import choice

OUTPUT_FILENAME = "output.txt"
MATRIX_FILENAME = "count.bin"
WORD_LIST_FILENAME = "words_fr.txt"

def initiate(word_list):
    count = np.zeros((256,256,256),dtype='int32')
    with codecs.open(word_list, "r", "utf-8") as lines:
        for l in  lines:
            i=0
            j=0
            for k in [ord(c) for c in list(l)]:
                count[i,j,k] += 1
                i = j
                j = k
    count.tofile(MATRIX_FILENAME)

# Build a dictionnary to check whether word already exists
def create_dictionary(word_list):
    dico = []
    with codecs.open(word_list, "r", "utf-8") as lines:
        for l in  lines:
            dico.append(l[:-1])
    return dico
 
# Load the trigram count matrix and normalize it
def load_trigrams():
    count = np.fromfile(MATRIX_FILENAME,dtype="int32").reshape(256,256,256)
    s=count.sum(axis=2)
    st=np.tile(s.T,(256,1,1)).T
    p=count.astype('float')/st
    p[np.isnan(p)]=0
    return p

# Build words
def build_word(word_length,dico,trigrams):
    i=0
    j=0
    res = u''
    while not j==10:
        k=choice(range(256),1,p=trigrams[i,j,:])[0]
        res = res + chr(k)
        i=j
        j=k
    if len(res) == 1+word_length:
        if res[:-1] in dico:
            x=res[:-1]+"*"
        else:
            x=res[:-1]
        return res

def generate_list(word_length,count,dico,trigrams):
    f = codecs.open(OUTPUT_FILENAME,"w","utf-8")
    for i in range(count):
        f.write(build_word(word_length,dico,trigrams)+"\n")
    f.close()

def main():
    initiate(WORD_LIST_FILENAME)
    dictionary = create_dictionary(WORD_LIST_FILENAME)
    trigrams = load_trigrams()
    generate_list(7,20,dictionary,trigrams)

if __name__ == "__main__":
    main()
