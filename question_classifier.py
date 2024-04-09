#!/usr/bin/env python
# coding=utf-8
# programmer:Jarsore,04/07/2024

# 分类


import os
import ahocorasick#调用这个库函数，可以网上搜索这个函数库用法

class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])


        #　特征词路径
        self.dish_path = os.path.join(cur_dir, 'dict/dish.txt')  # 美食
        self.restaurant_path = os.path.join(cur_dir, 'dict/restaurant.txt') # 餐厅
        self.ingredient_path = os.path.join(cur_dir, 'dict/ingredient.txt') # 食材
        self.chef_path = os.path.join(cur_dir, 'dict/chef.txt') # 厨师
        self.cuisine_path = os.path.join(cur_dir, 'dict/cuisine.txt') # 菜系
        self.flavor_path = os.path.join(cur_dir, 'dict/flavor.txt') # 口味

        self.deny_path = os.path.join(cur_dir, 'dict/deny.txt')#否认

        # self.disease_path = os.path.join(cur_dir, 'dict/disease.txt')#疾病
        # self.department_path = os.path.join(cur_dir, 'dict/department.txt')#科室
        # self.check_path = os.path.join(cur_dir, 'dict/check.txt')#检查
        # self.drug_path = os.path.join(cur_dir, 'dict/drug.txt')#药物
        # self.food_path = os.path.join(cur_dir, 'dict/food.txt')#食物
        # self.producer_path = os.path.join(cur_dir, 'dict/producer.txt')#药品大类
        # self.symptom_path = os.path.join(cur_dir, 'dict/symptom.txt')#症状


        # 加载特征词
        self.dish_wds= [i.strip() for i in open(self.dish_path,encoding="utf-8") if i.strip()] #encoding="utf-8"
        self.restaurant_wds= [i.strip() for i in open(self.restaurant_path,encoding="utf-8") if i.strip()]
        self.ingredient_wds = [i.strip() for i in open(self.ingredient_path, encoding="utf-8") if i.strip()]
        self.chef_wds = [i.strip() for i in open(self.chef_path, encoding="utf-8") if i.strip()]
        self.cuisine_wds = [i.strip() for i in open(self.cuisine_path, encoding="utf-8") if i.strip()]
        self.flavor_wds = [i.strip() for i in open(self.flavor_path, encoding="utf-8") if i.strip()]
        self.region_words = set(self.dish_wds + self.restaurant_wds + self.ingredient_wds + self.chef_wds + self.cuisine_wds + self.flavor_wds)
        self.deny_words = [i.strip() for i in open(self.deny_path,encoding="utf-8") if i.strip()]

        # self.disease_wds= [i.strip() for i in open(self.disease_path,encoding="utf-8") if i.strip()] #encoding="utf-8"
        # self.department_wds= [i.strip() for i in open(self.department_path,encoding="utf-8") if i.strip()]
        # self.check_wds= [i.strip() for i in open(self.check_path,encoding="utf-8") if i.strip()]
        # self.drug_wds= [i.strip() for i in open(self.drug_path,encoding="utf-8") if i.strip()]
        # self.food_wds= [i.strip() for i in open(self.food_path,encoding="utf-8") if i.strip()]
        # self.producer_wds= [i.strip() for i in open(self.producer_path,encoding="utf-8") if i.strip()]
        # self.symptom_wds= [i.strip() for i in open(self.symptom_path,encoding="utf-8") if i.strip()]
        # self.region_words = set(self.department_wds + self.disease_wds + self.check_wds + self.drug_wds + self.food_wds + self.producer_wds + self.symptom_wds)
        # self.deny_words = [i.strip() for i in open(self.deny_path,encoding="utf-8") if i.strip()]



        # 构造领域actree，基于树匹配比关键词分割匹配更高效，ahocorasick是个现成的快速匹配函数
        self.region_tree = self.build_actree(list(self.region_words))#调用下面的build_actre函数
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()#调用下面定义的build_wdtype_dict函数，构造词类型

        # 问句疑问词
        self.dish_qwds = ['食物', '食品', '填饱肚子的东西', '美食', '早餐','午餐','晚餐','夜宵','吃食','菜肴']
        self.restaurant_qwds = ['饭店', '餐馆', '小吃店', '食堂', '美食城','饮食广场','酒店']
        self.ingredient_qwds = ['食材', '材料', '蔬菜', '肉类', '菌类','水果','主食']
        self.chef_qwds = ['厨师', '厨子', '伙夫', '做菜的人', '美食家']
        self.cuisine_qwds = ['地方菜', '菜系', '哪儿']
        self.flavor_qwds = ['口味', '清淡', '现象', '症候', '表现']

        # self.flavor_qwds = ['症状', '表征', '现象', '症候', '表现']


        # self.symptom_qwds = ['症状', '表征', '现象', '症候', '表现']
        # self.cause_qwds = ['原因','成因', '为什么', '怎么会', '怎样才', '咋样才', '怎样会', '如何会', '为啥', '为何', '如何才会', '怎么才会', '会导致', '会造成']
        # self.acompany_qwds = ['并发症', '并发', '一起发生', '一并发生', '一起出现', '一并出现', '一同发生', '一同出现', '伴随发生', '伴随', '共现']
        # self.food_qwds = ['饮食', '饮用', '吃', '食', '伙食', '膳食', '喝', '菜' ,'忌口', '补品', '保健品', '食谱', '菜谱', '食用', '食物','补品']
        # self.drug_qwds = ['药', '药品', '用药', '胶囊', '口服液', '炎片']
        # self.prevent_qwds = ['预防', '防范', '抵制', '抵御', '防止','躲避','逃避','避开','免得','逃开','避开','避掉','躲开','躲掉','绕开',
        #                      '怎样才能不', '怎么才能不', '咋样才能不','咋才能不', '如何才能不',
        #                      '怎样才不', '怎么才不', '咋样才不','咋才不', '如何才不',
        #                      '怎样才可以不', '怎么才可以不', '咋样才可以不', '咋才可以不', '如何可以不',
        #                      '怎样才可不', '怎么才可不', '咋样才可不', '咋才可不', '如何可不']
        # self.lasttime_qwds = ['周期', '多久', '多长时间', '多少时间', '几天', '几年', '多少天', '多少小时', '几个小时', '多少年']
        # self.cureway_qwds = ['怎么治疗', '如何医治', '怎么医治', '怎么治', '怎么医', '如何治', '医治方式', '疗法', '咋治', '怎么办', '咋办', '咋治']
        # self.cureprob_qwds = ['多大概率能治好', '多大几率能治好', '治好希望大么', '几率', '几成', '比例', '可能性', '能治', '可治', '可以治', '可以医']
        # self.easyget_qwds = ['易感人群', '容易感染', '易发人群', '什么人', '哪些人', '感染', '染上', '得上']
        # self.check_qwds = ['检查', '检查项目', '查出', '检查', '测出', '试出']
        # self.belong_qwds = ['属于什么科', '属于', '什么科', '科室']
        # self.cure_qwds = ['治疗什么', '治啥', '治疗啥', '医治啥', '治愈啥', '主治啥', '主治什么', '有什么用', '有何用', '用处', '用途',
        #                   '有什么好处', '有什么益处', '有何益处', '用来', '用来做啥', '用来作甚', '需要', '要']



        print('model init finished ......')

        return



    '''分类主函数'''
    def classify(self, question):

        data = {}

        food_dict = self.check_food(question)  # 调用下面定义的check_medical问句过滤函数
        # medical_dict = self.check_medical(question)#调用下面定义的check_medical问句过滤函数

        if not food_dict:
            return {}
        # if not medical_dict:
        #     return {}

        data['args'] = food_dict
        # data['args'] = medical_dict

        #收集问句当中所涉及到的实体类型
        types = []

        # for type_ in medical_dict.values():
        for type_ in food_dict.values():
            types += type_

        question_type = 'others'#这句话无意义
        question_types = []





        # 餐厅_restaurant
        # 某个菜肴在哪家餐厅卖？
        if self.check_words(self.dish_qwds, question) and ('restaurant' in types):#self.dish_qwds来自于init，查找self.dish_qwds是否在question内
            # 前面检测问句中是否有食物
            question_type = 'dish_restaurant'
            question_types.append(question_type)
        # 某个餐厅卖什么菜肴？
        if self.check_words(self.dish_qwds, question) and ('dish' in types):#check_words是下面定义的特征词分类函数
            question_type = 'restaurant_dish'
            question_types.append(question_type)

        # 食材_ingredient
        # 某个美食需要哪些食材来制作？
        if self.check_words(self.ingredient_qwds, question) and ('dish' in types):#self.dish_qwds来自于init，查找self.dish_qwds是否在question内
            question_type = 'dish_ingredient'
            question_types.append(question_type)

        # 厨师_chef
        if self.check_words(self.chef_qwds, question) and ('dish' in types):#self.dish_qwds来自于init，查找self.dish_qwds是否在question内
            question_type = 'dish_chef'
            question_types.append(question_type)

        # 地方菜_cuisine
        if self.check_words(self.cuisine_qwds, question) and ('dish' in types):#self.dish_qwds来自于init，查找self.dish_qwds是否在question内
            question_type = 'dish_cuisine'
            question_types.append(question_type)

        # 口味_flavor
        if self.check_words(self.flavor_qwds, question) and ('dish' in types):#self.dish_qwds来自于init，查找self.dish_qwds是否在question内
            question_type = 'dish_flavor'
            question_types.append(question_type)




        # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        if question_types == [] and 'dish' in types:
            question_types = ['dish_desc']

        # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        if question_types == [] and 'restaurant' in types:
            question_types = ['dish_restaurant']

        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        return data


    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()

        for wd in self.region_words:#找到用户输入的词是什么范围的，比如用户输入高血压，这个单词属于疾病？食物？科室？还是药物
            wd_dict[wd] = []


            if wd in self.dish_wds:
                wd_dict[wd].append('dish')
            if wd in self.restaurant_wds:
                wd_dict[wd].append('restaurant')
            if wd in self.ingredient_wds:
                wd_dict[wd].append('ingredient')
            if wd in self.chef_wds:
                wd_dict[wd].append('chef')
            if wd in self.cuisine_wds:
                wd_dict[wd].append('cuisine')
            if wd in self.flavor_wds:
                wd_dict[wd].append('flavor')

        return wd_dict

    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):

        actree = ahocorasick.Automaton() # 初始化trie树，ahocorasick 库 ac自动化 自动过滤违禁数据
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))   # 向trie树中添加单词
        actree.make_automaton()   # 将trie树转化为Aho-Corasick自动机

        return actree

    '''问句过滤'''
    def check_food(self, question):

        region_wds = []
        for i in self.region_tree.iter(question):   # ahocorasick库 匹配问题  iter返回一个元组，i的形式如(3, (23192, '乙肝'))
            wd = i[1][1]  # 匹配到的词
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)   # stop_wds取重复的短的词，如region_wds=['乙肝', '肝硬化', '硬化']，则stop_wds=['硬化']
        final_wds = [i for i in region_wds if i not in stop_wds]     # final_wds取长词
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}#来自于构造词典，# 获取词和词所对应的实体类型

        return final_dict

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):

        for wd in wds:
            if wd in sent:
                return True

        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)