#!/usr/bin/env python
# coding=utf-8
# programmer:Jarsore,04/07/2024

# 问句分类


import os
import ahocorasick # 调用这个库函数，可以网上搜索这个函数库用法


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

        self.deny_path = os.path.join(cur_dir, 'dict/deny.txt') # 否认


        # 加载特征词
        self.dish_wds= [i.strip() for i in open(self.dish_path,encoding="utf-8") if i.strip()] # encoding="utf-8"
        self.restaurant_wds= [i.strip() for i in open(self.restaurant_path,encoding="utf-8") if i.strip()]
        self.ingredient_wds = [i.strip() for i in open(self.ingredient_path, encoding="utf-8") if i.strip()]
        self.chef_wds = [i.strip() for i in open(self.chef_path, encoding="utf-8") if i.strip()]
        self.cuisine_wds = [i.strip() for i in open(self.cuisine_path, encoding="utf-8") if i.strip()]
        self.flavor_wds = [i.strip() for i in open(self.flavor_path, encoding="utf-8") if i.strip()]
        self.region_words = set(self.dish_wds + self.restaurant_wds + self.ingredient_wds + self.chef_wds + self.cuisine_wds + self.flavor_wds)
        self.deny_words = [i.strip() for i in open(self.deny_path,encoding="utf-8") if i.strip()]


        # 构造领域actree，基于树匹配比关键词分割匹配更高效，ahocorasick是个现成的快速匹配函数
        self.region_tree = self.build_actree(list(self.region_words)) # 调用下面的build_actre函数
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict() # 调用下面定义的build_wdtype_dict函数，构造词类型

        '''
        可能出现的问句：
        1.红烧肉哪家餐馆有卖？
        2.红烧肉的原材料是啥？
        3.做红烧肉的人是谁？
        4.红烧肉是哪儿的菜？
        5.红烧肉是什么味道？
        6.有什么好吃的菜
        '''

        # 问句疑问词
        self.dish_qwds = ['食物', '食品', '美食', '菜','好吃的','吃食','菜肴']
        self.restaurant_qwds = ['饭店', '餐馆', '小吃店', '食堂', '餐厅','饮食广场','酒店','哪家']
        self.ingredient_qwds = ['食材', '材料', '原材料','蔬菜', '肉类', '菌类','水果','主食','用什么做']
        self.chef_qwds = ['厨师', '厨子', '做菜的人','是谁做的']
        self.cuisine_qwds = ['地方菜', '菜系', '哪儿','是什么菜']
        self.flavor_qwds = ['口味', '味道','味道如何', '尝起来怎么样', '甜不甜', '咸不咸']

        # 在这里我少了一些问句疑问词，这里有问题需要修改
        # self.flavor_qwds = ['口味', '味道', '尝起来怎么样', '甜不甜', '咸不咸']

        print('model init finished ......')
        return


    '''分类主函数'''
    def classify(self, question):

        data = {}

        food_dict = self.check_food(question)  # 调用下面定义的check_food问句过滤函数

        if not food_dict:
            return {}

        data['args'] = food_dict

        # 收集问句当中所涉及到的实体类型
        types = []

        # for type_ in medical_dict.values():
        for type_ in food_dict.values():
            types += type_

        question_type = 'others' # 这句话无意义
        question_types = []


        # 餐厅_restaurant
        # 某个菜肴在哪家餐厅卖？
        if self.check_words(self.restaurant_qwds, question) and ('dish' in types): # self.dish_qwds来自于init，查找self.dish_qwds是否在question内
            # 前面检测问句中是否有餐厅疑问词，and后面是收集问句中出现的实体类型
            question_type = 'dish_restaurant'
            question_types.append(question_type)
        # 某个餐厅卖什么菜肴？
        if self.check_words(self.dish_qwds, question) and ('restaurant' in types): # check_words是下面定义的特征词分类函数
            question_type = 'restaurant_dish'
            question_types.append(question_type)

        # 食材_ingredient
        # 某个美食需要哪些食材来制作？
        if self.check_words(self.ingredient_qwds, question) and ('dish' in types): # self.dish_qwds来自于init，查找self.dish_qwds是否在question内
            question_type = 'dish_ingredient'
            question_types.append(question_type)

        # 厨师_chef
        # 做某个美食的厨师是谁？
        if self.check_words(self.chef_qwds, question) and ('dish' in types):
            question_type = 'dish_chef'
            question_types.append(question_type)

        # 地方菜_cuisine
        # 某个美食是哪儿的地方菜？
        if self.check_words(self.cuisine_qwds, question) and ('dish' in types):
            question_type = 'dish_cuisine'
            question_types.append(question_type)

        # 口味_flavor
        # 某个美食尝起来什么味道？
        if self.check_words(self.flavor_qwds, question) and ('dish' in types):
            question_type = 'dish_flavor'
            question_types.append(question_type)


        # 若没有查到相关的外部查询信息，那么则将该美食的描述信息返回
        if question_types == [] and 'dish' in types:
            question_types = ['dish_desc']

        # # 若没有查到相关的外部查询信息，那么则将什么信息返回？
        # if question_types == [] and 'restaurant' in types:
        #     question_types = ['dish_restaurant']

        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        return data


    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()

        for wd in self.region_words: # 找到用户输入的词是什么范围的，比如用户输入高血压，这个单词属于疾病？食物？科室？还是药物
            wd_dict[wd] = []

            # 判断用户问句中的特征词
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
    # 该方法的作用是将给定的单词列表[]构建成一个 Aho-Corasick 自动机，以便后续用于高效地进行单词匹配和查找操作。
    def build_actree(self, wordlist):

        actree = ahocorasick.Automaton() # 初始化trie树，ahocorasick库 ac自动化 自动过滤违禁数据
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))   # 向trie树中添加单词
        actree.make_automaton()   # 将trie树转化为Aho-Corasick自动机

        return actree


    '''问句过滤'''
    # 该方法的主要功能是从问题中提取涉及食物的关键词，并将其与相应的实体类型进行匹配和存储，最终返回一个包含关键词和对应实体类型的字典。
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
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds} # 来自于构造词典，# 获取词和词所对应的实体类型

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
