#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : preprocess.py
# @Description: data analysis preprocess and flow control class
# @Software: PyCharm
# @Author  : Mengran Li
# @Time    : 2019/10/27
# @Version : 1.0

import os
from bs4 import BeautifulSoup
import SPIMI, Merge
from SPIMI import spimi_implement
from search import search


class preprocess:

    # This method is to read files in folder and seperate articles according to block size limitation
    def readFiles(self):
        folder = os.path.exists("reuters21578")
        BASEPATH = "reuters21578/"
        Block_size = 500

        if not folder:
            print("********NO SUCH FOLDER CAN BE FOUND********")

        else:
            files = os.listdir("reuters21578")
            files=sorted(files)
            for item in files:
                if item.endswith(".sgm"):
                    print(item)
                    stream = open(BASEPATH + item, encoding="latin-1")
                    content = stream.read()
                    soup_content = BeautifulSoup(content, "html.parser")
                    articles = soup_content.find_all('reuters')
                    block_first = {}
                    for i in range(0, Block_size):
                        self.separateArticles(articles[i], block_first)
                    spimi_implement(block_first)
                    block_second = {}
                    for i in range(Block_size, len(articles)):
                        self.separateArticles(articles[i], block_second)
                    spimi_implement(block_second)

    # This method is to match article pattern and extract articles with ID from raw data
    def separateArticles(self, a, block):
        body = ""
        title = ""
        newID = a['newid']
        if not a.title is None:
            title = a.title.string
        if not a.body is None:
            body = a.body.string
        article = title + " " + body
        block[newID] = article

    # main is used to fow control
    def main(self):
        print("============ begin to read files ================")
        self.readFiles()
        SPIMI.output_to_file()
        print("============ begin to merge blocks ==============")
        Merge.merge_blocks()
        print("============ merge finished======================")
        print("============= statistical properties ============")
        SPIMI.statistical_table()
        while (True):
            print("======== choose your command =======")
            print("=============1. search  ============")
            print("=============2. quit  ==============")
            order = int(input())
            if order == 1:
                print("====== please input the query ======")
                print("valid input example: (word) or (word1 and word2) or (word1 or word2)")
                query = str(input())
                if query == "":
                    print("============= empty query ==============")
                    continue
                else:
                    search(query)

            elif order == 2:
                break
            else:
                print("============= invalid input ==============")


if __name__ == "__main__":
    t = preprocess()
    t.main()
