# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    :LossyCompression.py
# @Description: lossy compression include remove punctuation, remove number, remove special characters and stop words
# @Software: PyCharm
# @Author  : Mengran Li
# @Time    : 2019/10/27
# @Version : 1.0
import re
from string import punctuation



def clean_num_character(str):
    return re.sub('[0-9’!#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+', "", str)


def clean_empty(str):
    return re.sub("[^A-Za-z0-9]", " ", str)


def clean_word(tokens):
    text = tokens
    text = [token for token in text if not token in punctuation]
    text = filter(None, text)
    text = [token for token in text if not token == "''" and not token == '``']
    text=[token for token in text  if not token == "\x03" and not token == "\x7f"]
    text = [token for token in text if not token.isdigit()]
    text = [token.lower() for token in text]
    return text


def clean_number(tokens):
    text = tokens
    text = [token for token in text if not token.isdigit()]
    return text


def case_folding(tokens):
    text = tokens
    text = [token.lower() for token in text]
    return text


def get_stopwords(index, num):
    # for k in sorted(d, key=lambda k: len(d[k]), reverse=True):
    stop_words = []
    key_list = []
    for item in sorted(index, key=lambda item: len(index[item]), reverse=True):
        key_list.append(item)

    for i in range(num):
        stop_words.append(key_list[i])
    stop_words.append("aa")
    stop_words.append("aaa")

    return stop_words


def remove_stopwords(index, num):
    term_no_stopword = {}
    stop_words = get_stopwords(index, num)

    for each in index.keys():
        if each not in stop_words:
            term_no_stopword[each] = index[each]

    return term_no_stopword
