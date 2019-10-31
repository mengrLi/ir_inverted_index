#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : SPIMI.py
# @Description: implement SPIMI algorithm and finish the table
# @Software: PyCharm
# @Author  : Mengran Li
# @Time    : 2019/10/27
# @Version : 1.0

import os
from LossyCompression import clean_num_character, clean_number, clean_empty, case_folding, remove_stopwords
import nltk
import collections
import json

nonposit_blocks = []
posit_blocks = []
nonumber_blocks = []
nonumber_postblocks = []
lower_blocks = []
lower_posit_blocks = []

# This method is to create non-positioal dictioanry for each block, the second colum of table
def create_nonpositional(token, id, dict):
    if token not in dict:
        posting_list = []
        posting_list.append(id)
        dict[token] = posting_list
    else:
        posting_list = dict[token]
        if id not in posting_list:
            posting_list.append(id)
            dict[token] = posting_list

# This method is to create positioal dictioanry for each block, the third colum of table
def create_positional(token, id, positdict):
    if token not in positdict:
        posting_list = []
        posting_list.append(id)
        positdict[token] = posting_list
    else:
        posting_list = positdict[token]
        posting_list.append(id)
        positdict[token] = posting_list

# this method is to sort complete index by keys
def sort_dict(unfiltered_dict):
    result = collections.OrderedDict(sorted(unfiltered_dict.items()))
    return result

# SPIMI algorithm inplementation and data clean process
def spimi_implement(block_dict):
    unfiltered_nondict = {}
    unfiltered_positdict = {}
    nonumber_nondict = {}
    nonumber_positdict = {}
    lower_dict = {}
    lower_posit_dict = {}
    for key in block_dict:
        text = clean_empty(str(block_dict[key]))
        tokens = nltk.word_tokenize(text)

        nonum_text = clean_num_character(text)
        nonumber_tokens = nltk.word_tokenize(nonum_text)
        nodigital_tokens = clean_number(nonumber_tokens)

        lower_tokens = case_folding(nonumber_tokens)
        id = key
        # unfiltered text
        for token in tokens:
            if token.strip() == '':
                continue
            create_nonpositional(token, id, unfiltered_nondict)
            create_positional(token, id, unfiltered_positdict)
        for token in nodigital_tokens:
            create_nonpositional(token, id, nonumber_nondict)
            create_positional(token, id, nonumber_positdict)

        for token in lower_tokens:
            create_nonpositional(token, id, lower_dict)
            create_positional(token, id, lower_posit_dict)

    nonposit_blocks.append(sort_dict(unfiltered_nondict))
    posit_blocks.append(sort_dict(unfiltered_positdict))
    nonumber_blocks.append(sort_dict(nonumber_nondict))
    nonumber_postblocks.append(sort_dict(nonumber_positdict))
    lower_blocks.append(sort_dict(lower_dict))
    lower_posit_blocks.append(sort_dict(lower_posit_dict))


# this method is to add all blocks together to fill in the table
def merge_index(blocks, index):
    for item in blocks:
        for key in item.keys():
            if key not in index.keys():
                posting_list = []
                for i in item[key]:
                    posting_list.append(i)
                    index[key] = posting_list
            else:
                temp = index[key]
                for i in item[key]:
                    temp.append(i)
                    index[key] = temp

# this method is to calculate reduction
def calculate_reduction(num1, num2, num3):
    return -round(float((num1 - num2) / num3) * 100, 3)

# this method is to calculate T
def calculate_T(num1, num2):
    return -round(float((num1 - num2) / num1) * 100, 3)


def calculate_length(index):
    length = 0
    for item in index:
        length = length + len(index[item])
    return length

# this method is  to calculate statistical properties
def statistical_table():
    global unfiltered_index, unfil_post_index, nonumber_index, nonumber_post_index, lower_index, lower_posit_index
    unfiltered_index = {}
    unfil_post_index = {}
    nonumber_index = {}
    nonumber_post_index = {}
    lower_index = {}
    lower_posit_index = {}

    merge_index(nonposit_blocks, unfiltered_index)
    merge_index(posit_blocks, unfil_post_index)
    merge_index(nonumber_blocks, nonumber_index)
    merge_index(nonumber_postblocks, nonumber_post_index)
    merge_index(lower_blocks, lower_index)
    merge_index(lower_posit_blocks, lower_posit_index)

    unfiltered_terms = len(unfiltered_index)
    unfiltered_nonposition = calculate_length(unfiltered_index)
    unfiltered_positional = calculate_length(unfil_post_index)

    nonumber_terms = len(nonumber_index)
    nonumber_nonposition = calculate_length(nonumber_index)
    nonumber_position = calculate_length(nonumber_post_index)

    lower_terms = len(lower_index)
    lower_nonpositinal = calculate_length(lower_index)
    lower_positional = calculate_length(lower_posit_index)

    remove_30_index = remove_stopwords(lower_index, 30)
    remove_30_posit_index = remove_stopwords(lower_posit_index, 30)
    remove_30terms = len(remove_30_index)
    remove_30nonpositional = calculate_length(remove_30_index)
    remove_30positional = calculate_length(remove_30_posit_index)

    remove_150_index = remove_stopwords(lower_index, 150)
    remove_150_posit_index = remove_stopwords(lower_posit_index, 150)
    remove_150terms = len(remove_150_index)
    remove_150nonpositional = calculate_length(remove_150_index)
    remove_150positional = calculate_length(remove_150_posit_index)

    print("---number of---", "        ", "distinct(terms)", "      ", "     ", "non-positional", "      ",
          "     ", "tokens(positional)", "      ")
    print("               ", "number ", "reduction%  ", " T% ", "number   ", " reduction% ", " T%  ",
          "  number  ", "reduction%", " T% ")
    print("unfiltered     ", str(unfiltered_terms), "         ", "          ", str(unfiltered_nonposition),
          "          ", "          ",
          str(unfiltered_positional), "          ", "         ")

    nonumber_reduction = calculate_reduction(unfiltered_terms, nonumber_terms, unfiltered_terms)
    nonumber_T = calculate_T(unfiltered_terms, nonumber_terms)
    nonum_nonposit_reduction = calculate_reduction(unfiltered_nonposition, nonumber_nonposition, unfiltered_nonposition)
    nonum_nonposit_T = calculate_T(unfiltered_nonposition, nonumber_nonposition)
    nonum_posit_reduction = calculate_reduction(unfiltered_positional, nonumber_position, unfiltered_positional)
    nonum_posit_T = calculate_T(unfiltered_positional, nonumber_position)
    print("no number      ", str(nonumber_terms) + "   ", str(nonumber_reduction) + "  ", str(nonumber_T) + "  ",
          str(nonumber_nonposition) + "  ",
          str(nonum_nonposit_reduction) + "   ", str(nonum_nonposit_T) + "   ",
          str(nonumber_position) + "   ", str(nonum_posit_reduction) + "    ", str(nonum_posit_T) + "   ")

    lower_reduction = calculate_reduction(nonumber_terms, lower_terms, unfiltered_terms)
    lower_T = calculate_T(unfiltered_terms, lower_terms)
    lower_nonposit_reduction = calculate_reduction(nonumber_nonposition, lower_nonpositinal, unfiltered_nonposition)
    lower_nonposit_T = calculate_T(unfiltered_nonposition, lower_nonpositinal)
    lower_posit_reduction = calculate_reduction(nonumber_position, lower_positional, unfiltered_positional)
    lower_posit_T = calculate_T(unfiltered_positional, lower_positional)
    print("case folding   ", str(lower_terms) + "   ", str(lower_reduction) + " ", str(lower_T) + "  ",
          str(lower_nonpositinal) + "  ",
          str(lower_nonposit_reduction) + "   ", str(lower_nonposit_T) + "   ",
          str(lower_positional) + "   ", str(lower_posit_reduction) + "      ", str(lower_posit_T) + "   ")

    stop30_reduction = calculate_reduction(lower_terms, remove_30terms, unfiltered_terms)
    stop30_T = calculate_T(unfiltered_terms, remove_30terms)
    stop30_nonposit_reduction = calculate_reduction(lower_nonpositinal, remove_30nonpositional, unfiltered_nonposition)
    stop30_nonposit_T = calculate_T(unfiltered_nonposition, remove_30nonpositional)
    stop30_posit_reduction = calculate_reduction(lower_positional, remove_30positional, unfiltered_positional)
    stop30_posit_T = calculate_T(unfiltered_positional, remove_30positional)
    print("30 stop words  ", str(remove_30terms) + "   ", str(stop30_reduction) + "  ", str(stop30_T) + " ",
          str(remove_30nonpositional) + "  ",
          str(stop30_nonposit_reduction) + "  ", str(stop30_nonposit_T) + "  ",
          str(remove_30positional) + "   ", str(stop30_posit_reduction) + "   ", str(stop30_posit_T) + "   ")

    stop150_reduction = calculate_reduction(remove_30terms, remove_150terms, unfiltered_terms)
    stop150_T = calculate_T(unfiltered_terms, remove_150terms)
    stop150_nonposit_reduction = calculate_reduction(remove_30nonpositional, remove_150nonpositional,
                                                     unfiltered_nonposition)
    stop150_nonposit_T = calculate_T(unfiltered_nonposition, remove_150nonpositional)
    stop150_posit_reduction = calculate_reduction(remove_30positional, remove_150positional, unfiltered_positional)
    stop150_posit_T = calculate_T(unfiltered_positional, remove_150positional)
    print("150stop words  ", str(remove_150terms) + "   ", str(stop150_reduction) + "  ", str(stop150_T) + "  ",
          str(remove_150nonpositional) + "  ",
          str(stop150_nonposit_reduction) + "   ", str(stop150_nonposit_T) + "   ",
          str(remove_150positional) + "   ", str(stop150_posit_reduction) + "   ", str(stop150_posit_T) + "   ")

# This is method is write all blocks to files in BLOCK folder
def output_to_file():
    global file_num
    file_num = 1
    for item in lower_blocks:
        item = remove_stopwords(item, 150)
        path = "BLOCK/"
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)
        file_name = os.path.join(path, str(file_num) + ".txt")
        jsonString = json.dumps(item, default=lambda obj: obj.__dict__, sort_keys=True, indent=4)
        fo = open(file_name, "w")
        fo.write(jsonString)
        fo.close()
        file_num += 1
