#!/usr/bin/env python
# coding=utf-8
# programmer:Jarsore,04/06/2024

# 读取图谱并返回结果

from py2neo import Graph

class AnswerSearcher:


    def __init__(self):#调用数据库进行查询
        # self.g = Graph("http://localhost:7474", username="neo4j", password="wang1985")#老版本neo4j
        self.g = Graph("http://localhost:7474", auth=("neo4j", "Neo4j2020."))#输入自己修改的用户名，密码
        self.num_limit = 20#最多显示字符数量

    '''执行cypher查询，并返回相应结果'''
    def search_main(self, sqls):

        final_answers = [] # 首先将最终答案定义为一个空列表

        for sql_ in sqls:

            question_type = sql_['question_type'] # sql_里面的关键字

            queries = sql_['sql'] # sql_是一个字典

            answers = []

            for query in queries:

                ress = self.g.run(query).data() # 运行图数据库，进行查询

                answers += ress

            final_answer = self.answer_prettify(question_type, answers) # 调用回复模板函数

            if final_answer:

                print(5)

                final_answers.append(final_answer)

        return final_answers

# 要修改的部分
    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answers):
        # answers是一个列表，里面的每一个元素是字典

        final_answer = []

        if not answers:
            print(4)
            return ''

        # 这段代码有问题，这段回复模板跟parser中的sql查询语句不匹配；

        # 以下两个elif与其他的不太一样
        if question_type == 'dish_restaurant':

            desc = [i['m.name'] for i in answers]
            subject = answers[0]['m.restaurant']
            final_answer = '餐厅{0}售卖的美食有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        # elif question_type == 'restaurant_dish':
        #
        #     desc = [i['m.name'] for i in answers]
        #     subject = answers[0]['n.name']
        #     final_answer = '有美食{0}售卖的餐厅有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))


        elif question_type == 'dish_ingredient':

            desc = [i['n.name'] for i in answers] # 这段代码待定
            subject = answers[0]['m.name']
            final_answer = '{0}的食材包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
            # 上一行代码中的{0}指代subject

        elif question_type == 'dish_chef':

            desc = [i['m.name'] for i in answers]
            subject = answers[0]['m.chef']
            final_answer = '厨师{0}会做的菜肴有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))



        # 交换m后面位置
        elif question_type == 'dish_cuisine':

            desc = [i['m.name'] for i in answers]
            subject = answers[0]['m.cuisine']
            final_answer = '美食{1}来自菜系：{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'dish_flavor':

            desc = [i['m.name'] for i in answers]
            subject = answers[0]['m.cuisine']
            final_answer = '美食{1}的口味是：{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'dish_dec':
            final_answer = "恭喜发财"




        return final_answer

if __name__ == '__main__':
    searcher = AnswerSearcher()
