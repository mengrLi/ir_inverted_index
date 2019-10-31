# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : search.py
# @Description: search queries in index and return the result
# @Software: PyCharm
# @Author  : Mengran Li
# @Time    : 2019/10/27
# @Version : 1.0
import json
import nltk
from LossyCompression import clean_word

BASEPATH = "INDEX/"

first_of_index = []

# this method is to implement single word search and sort the result
# read the index from index file by comparing the first item in index
def single_word_search(query_list):
    global first_of_index
    word = query_list[0]
    result = []
    if word < first_of_index[1]:
        index = read_index(1)
        if word in index.keys():
            for i in index[word]:
                result.append(int(i))

    else:
        index = read_index(2)
        if word in index.keys():
            for i in index[word]:
                result.append(int(i))

    return result

# this method is to implement and(intersection) search for multiple keywords
def And_operator(query_list):
    result = {}
    final_result = []
    num = 0
    for item in query_list:
        if item != "and":
            tmp = []
            tmp.append(item)
            num = num + 1
            list = single_word_search(tmp)
            for i in list:
                if i not in result.keys():
                    result[i] = 1
                else:
                    result[i] = result[i] + 1
    for key in result:
        if result[key] == num:
            final_result.append(int(key))
    number = len(final_result)
    print("There are  " + str(number) + "  articles are found!")
    print(sorted(final_result))


# this method is to implement or(union) search for multiple keywords
def Or_operator(query_list):
    result = {}
    num = 0
    for item in query_list:
        if item != "or":
            tmp = []
            tmp.append(item)
            num = num + 1
            list = single_word_search(tmp)
            for i in list:
                if i not in result.keys():
                    result[i] = 1
                else:
                    result[i] = result[i] + 1

    size = len(result.keys())
    print("There are  " + str(size) + "  articles are found!")
    while num > 0:
        final_result = []
        for key in result:
            if result[key] == num:
                final_result.append(int(key))
        print("find " + str(num) + " times")
        print(sorted(final_result))
        num = num - 1

# seperate different kinds of multiple search
def multiple_search(query_list):
    for i in query_list:
        if i == "and":
            And_operator(query_list)
            break
        elif i == "or":
            Or_operator(query_list)
            break


def read_index(flag):
    if flag == 1:
        stream = open(BASEPATH + "result1.txt", encoding="latin-1")
        content = stream.read()
        index_dict = json.loads(content)
        return index_dict
    else:
        stream = open(BASEPATH + "result2.txt", encoding="latin-1")
        content = stream.read()
        index_dict = json.loads(content)
        return index_dict


def get_first(item):
    global first_of_index
    for i in item:
        first_of_index.append(i)


def search(query):
    query_list = []
    tokens = nltk.word_tokenize(query)
    clean_queries = clean_word(tokens)
    for token in clean_queries:
        query_list.append(token)
    if len(query_list) == 0:
        print("=====invalid input, try again====")
    elif len(query_list) == 1:
        result = sorted(single_word_search(query_list))
        print("There are  " + str(len(result)) + "  articles are found!")
        print(result)
    else:
        multiple_search(query_list)
