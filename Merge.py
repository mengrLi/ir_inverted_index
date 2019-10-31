# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : Merge.py
# @Description: merge the block indexes into whole integrated index
# @Software: PyCharm
# @Author  : Mengran Li
# @Time    : 2019/10/27
# @Version : 1.0
import json
import os
from search import get_first

from Sort import Sorted

indexSizeLimit = 25000
BASEPATH = "BLOCK/"
processed_list = list(())

# read block files line by line
def merge_blocks():
    folder = os.path.exists(BASEPATH)
    if not folder:
        print("No folders find.")
    else:
        files = os.listdir(BASEPATH)
        for file in files:
            if file.endswith(".txt"):
                stream = open(BASEPATH + file, encoding="latin-1")
                content = stream.read()
                inverted_index = json.loads(content)
                processed_list.append(Sorted(inverted_index))
        merge_process()


def merge_process():
    inverted_index = {}
    global processed_list
    while (True):
        processed_list = list(filter(lambda each: each.is_empty() == False, processed_list))
        if len(processed_list) == 0:
            break
        top_item = get_min()
        inverted_index[top_item] = document_list(top_item)

    output_index(inverted_index)

# this method is to get the min key from processed list
def get_min():
    min_key = ""

    for item in processed_list:
        if min_key == "":
            min_key = item.get_min_key()
            continue

        if min_key > item.get_min_key():
            min_key = item.get_min_key()

    return min_key


def document_list(min_key):
    documentId_set = set(())

    for item in processed_list:
        if min_key == item.get_min_key():
            if len(documentId_set) == 0:
                documentId_set = set(item.get(min_key))

            else:
                for id in item.get(min_key):
                    documentId_set.add(id)
            item.remove_min_key(min_key)

    return list(documentId_set)


# this method is to write complete idex to file according to the index size limitation
def output_index(inverted_index):
    path = "INDEX/"
    folder = os.path.exists(path)
    item=[]
    first_item = list(inverted_index.keys())[0]
    second_item= list(inverted_index.keys())[indexSizeLimit+1]
    item.append(first_item)
    item.append(second_item)
    get_first(item)
    if not folder:
        os.makedirs(path)
    file_name = os.path.join(path, "result1.txt")
    first_part = dict(list(inverted_index.items())[0:indexSizeLimit])
    jsonString = json.dumps(first_part, default=lambda obj: obj.__dict__, sort_keys=True, indent=4)
    fo = open(file_name, "w")
    fo.write(jsonString)
    file_name = os.path.join(path, "result2.txt")
    second_part = dict(list(inverted_index.items())[indexSizeLimit + 1:-1])
    jsonString = json.dumps(second_part, default=lambda obj: obj.__dict__, sort_keys=True, indent=4)
    fo = open(file_name, "w")
    fo.write(jsonString)
    fo.close()
