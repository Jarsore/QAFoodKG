#!/usr/bin/env python
# coding=utf-8
# programmer:Jarsore,04/09/2024

# 解析

class QuestionPaser:

    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)
        return entity_dict



    '''解析主函数'''
    def parser_main(self, res_classify):

        args = res_classify['args']
        entity_dict = self.build_entitydict(args)#调用上面的构造实体节点函数
        question_types = res_classify['question_types']#需要question_classifier.py完成问题类型的识别
        sqls = []

        for question_type in question_types:
            sql_ = {}#注意与下面sql的区别，字典
            sql_['question_type'] = question_type
            sql = []


            if question_type == 'dish_restaurant':
                sql = self.sql_transfer(question_type, entity_dict.get('restaurant'))#sql_transfer是下面定义的分开处理问题子函数

            elif question_type == 'restaurant_dish':
                sql = self.sql_transfer(question_type, entity_dict.get('dish'))

            elif question_type == 'dish_ingredient':
                sql = self.sql_transfer(question_type, entity_dict.get('ingredient'))

            # ...

            elif question_type == 'dish_chef':
                sql = self.sql_transfer(question_type, entity_dict.get('chef'))
            elif question_type == 'dish_cuisine':
                sql = self.sql_transfer(question_type, entity_dict.get('cuisine'))
            elif question_type == 'dish_flavor':
                sql = self.sql_transfer(question_type, entity_dict.get('flavor'))




            elif question_type == 'dish_desc':
                sql = self.sql_transfer(question_type, entity_dict.get('dish'))

            elif question_type == 'dish_restaurant':
                sql = self.sql_transfer(question_type, entity_dict.get('restaurant'))



            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)

        return sqls#返回sql查询语句，可以是多条，给图谱


    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        sql = []


        # 查询售卖该菜肴的餐馆，在debug的时候，运行到对应的elif（说明已经找到合适的关系）会自动停止该函数的执行
        if question_type == 'dish_restaurant':
            sql = ["MATCH (m:Restaurant) where m.name = '{0}' return m.name, m.cause".format(i) for i in entities]#调用match语句

        # 查询某个餐厅卖什么食物
        elif question_type == 'restaurant_dish':
            sql = ["MATCH (m:Dish) where m.name = '{0}' return m.name, m.prevent".format(i) for i in entities]




        return sql


if __name__ == '__main__':
    handler = QuestionPaser()
