#!/usr/bin/env python
# coding=utf-8
# programmer:Jarsore,04/09/2024
# code url:

from question_classifier import *
from question_parser import *
from answer_search import *

#知识图谱美食问答系统

'''问答类'''
class FoodQASystemGraph:
    def __init__(self):
        self.classifier = QuestionClassifier() # 调用问题分类子函数，可以链接追踪
        self.parser = QuestionPaser() # 调用问题解析子函数
        self.searcher = AnswerSearcher() # 调用问题搜索子函数

    def chat_main(self, sent):
        answer = '抱歉，没能理解您的问题，我的词汇量有限，请输入更加标准的词语' # 这是初始答案
        res_classify = self.classifier.classify(sent) # 'sent'是用户的输入内容，利用classify函数先对其进行分类

        if not res_classify:
            print(1)
            return answer # 没有找到对应分类内容，返回初始答案
        ## 到上一步是没有问题的

        res_sql = self.parser.parser_main(res_classify) # 调用parser_main对内容进行解析

        final_answers = self.searcher.search_main(res_sql) # 对内容搜索合适的答案
        if not final_answers:
            print(2)
            return answer # 如果没有找到合适的最终答案，返回初始答案
        else:
            print(3)
            return '\n'.join(final_answers) # 连接字符

if __name__ == '__main__':
    handler = FoodQASystemGraph()
    while 1: # 进入一个死循环
        question = input('用户美食咨询:')
        answer = handler.chat_main(question)
        print('美食问答系统:', answer)

