#!/usr/bin/env python
# coding=utf-8
# programmer:Jarsore,04/03/2024

# 建立美食知识图谱

import os
import json
from py2neo import Graph, Node


class FoodGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])  # 获取当前绝对路径的上层目录
        self.data_path = os.path.join(cur_dir, 'data/food.json')  # 假设美食数据保存在'food.json'文件中
        self.g = Graph("http://localhost:7474", auth=("neo4j", "Neo4j2020."))  # 连接到Neo4j数据库

    '''读取文件'''
    def read_nodes(self):
        # 共6类节点
        # 定义美食知识图谱中的节点类型
        dishes = []  # 菜肴
        restaurants = []  # 餐厅
        ingredients = []  # 食材
        chefs = []  # 厨师
        cuisines = []  # 菜系
        flavors = []  # 口味

        dish_infos = []  # 美食信息

        # 定义美食知识图谱中的关系类型
        # 构建节点实体关系，共6类，food2.json
        rels_dish_ingredient = []  # 菜肴-食材关系
        rels_dish_restaurant = []  # 菜肴-餐厅关系
        rels_dish_chef = []  # 菜肴-厨师关系
        rels_dish_cuisine = []  # 菜肴-菜系关系
        rels_dish_flavor = []  # 菜肴-口味关系
        rels_restaurant_chef = []  # 餐厅-厨师关系

        count = 0
        for data in open(self.data_path,encoding='utf-8'):

            dish_dict = {}  # 空字典 **********

            count += 1
            print(count)
            data_json = json.loads(data) #读取数据

            dish = data_json['name']
            dish_dict['name'] = dish #美食字典的name是dish
            dishes.append(dish) #

            dish_dict['restaurant'] = '' #将餐厅描述字段的值设置为空字符串
            dish_dict['ingredients'] = ''
            dish_dict['chef'] = ''
            dish_dict['cuisine'] = '' #菜系
            dish_dict['flavor'] = '' #口味
            dish_dict['dec'] = ''

            # 查找一下词条是否在提取出来的文档段中，每一条文档段内容长度不一
            # 根据业务需求添加属性和关系
            if 'ingredients' in data_json: #食材

                dish_dict['ingredients'] = data_json['ingredients']

                ingredients += data_json['ingredients'] # 食材集合
                for ingredient in data_json['ingredients']:#用for循环的原因：一个美食可能对应好几个食材，手画图表示
                    rels_dish_ingredient.append([dish, ingredient])

            if 'restaurant' in data_json: #餐厅

                dish_dict['restaurant'] = data_json['restaurant']

                restaurant = data_json['restaurant']

                restaurants.append(restaurant)

                rels_dish_restaurant.append([dish, restaurant])

            if 'chef' in data_json: #厨师

                dish_dict['chef'] = data_json['chef']

                chef = data_json['chef']

                chefs.append(chef)

                rels_dish_chef.append([dish, chef])
                rels_restaurant_chef.append([restaurant, chef])

            if 'cuisine' in data_json: #菜系

                dish_dict['cuisine'] = data_json['cuisine']

                cuisine = data_json['cuisine']
                cuisines.append(cuisine)
                rels_dish_cuisine.append([dish, cuisine])

            if 'flavor' in data_json: #口味

                dish_dict['flavor'] = data_json['flavor']

                flavor = data_json['flavor']
                flavors.append(flavor)
                rels_dish_flavor.append([dish, flavor])

            if 'dec' in data_json:
                dish_dict['dec'] = data_json['dec']

            dish_infos.append(dish_dict) #添加美食信息list，dish_infos是一个列表，dish_dict是一个字典
        # print(dish_infos)

        # return (set(dishes),#美食元组
        #        set(restaurants),  #餐厅元组
        #         set(ingredients),  #食材元组
        #         set(chefs), #厨师元组
        #         rels_dish_cuisine, #美食-菜系实体关系
        #         rels_dish_flavor,  #美食-口味实体关系
        #         dish_infos,
        #         set(cuisines),  #菜系元组
        #         set(flavors), #口味元组
        #         rels_dish_ingredient,  #美食-食材实体关系
        #         rels_dish_restaurant,  #美食-餐厅实体关系
        #         rels_dish_chef,
        #         rels_restaurant_chef)

        return set(dishes), \
               set(restaurants),\
               set(ingredients),\
               set(chefs),\
               set(cuisines),  \
               set(flavors), \
               dish_infos, \
               rels_dish_ingredient, \
               rels_dish_restaurant, \
               rels_dish_chef, \
               rels_dish_cuisine,  \
               rels_dish_flavor,\
               rels_restaurant_chef


    '''建立节点'''
    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            count += 1
            print(count,len(nodes))
        return

    '''创建知识图谱中心美食的节点'''
    def create_dishes_nodes(self, dish_infos):
        count = 0
        # print(dish_infos)
        for dish_dict in dish_infos:
            # print(dish_dict)
            node = Node("Dish",
                        name=dish_dict['name'],# 名字
                        restaurant=dish_dict['restaurant'], # 餐厅
                        ingredient = dish_dict['ingredients'],  # 食材
                        chef = dish_dict['chef'],  # 厨师
                        cuisine = dish_dict['cuisine'],  # 菜系
                        flavor = dish_dict['flavor'],  # 口味
                        )#各个美食节点的属性
            self.g.create(node)
            count += 1
            print(count)
        return


    '''创建知识图谱实体节点类型schema,节点个数多，创建过程慢'''
    def create_graphnodes(self):

        Dishes, \
        Restaurants, \
        Ingredients, \
        Chefs, \
        Cuisines, \
        Flavors,\
        dish_infos,\
        rels_dish_ingredient, \
        rels_dish_restaurant, \
        rels_dish_chef,\
        rels_dish_cuisine,\
        rels_dish_flavor, \
        rels_restaurant_chef = self.read_nodes()

        # print(dish_infos)
        self.create_dishes_nodes(dish_infos)  # 调用上面的美食节点创建函数

        self.create_node('Dish', Dishes) #创建美食节点
        print(len(Dishes))
        self.create_node('Restaurant', Restaurants)
        print(len(Restaurants))
        self.create_node('Ingredient', Ingredients)
        print(len(Ingredients))
        self.create_node('Chef', Chefs) #厨师
        print(len(Chefs))
        self.create_node('Cuisine', Cuisines)
        print(len(Cuisines))
        self.create_node('Flavor', Flavors)
        print(len(Flavors))

        return


    '''创建实体关系边'''
    def create_graphrels(self):

        Dishes, \
        Restaurants, \
        Ingredients, \
        Chefs, \
        Cuisines, \
        Flavors, \
        dish_infos, \
        rels_dish_ingredient, \
        rels_dish_restaurant, \
        rels_dish_chef, \
        rels_dish_cuisine, \
        rels_dish_flavor, \
        rels_restaurant_chef = self.read_nodes()

        self.create_relationship('Dish', 'Restaurant', rels_dish_restaurant, 'now_sell', '提供该美食的餐厅')#调用下面的关系边创建函数
        self.create_relationship('Dish', 'Ingredient', rels_dish_ingredient, 'need_thing', '该美食需要的食材')
        self.create_relationship('Dish', 'Chef', rels_dish_chef, 'make_peo', '会做的厨师')
        self.create_relationship('Dish', 'Cuisine', rels_dish_cuisine, 'belong_to', '菜系')
        self.create_relationship('Dish', 'Flavor', rels_dish_flavor, 'taste_like', '口味')
        self.create_relationship('Restaurant','Chef',rels_restaurant_chef,'hire_peo','某餐厅的厨师')


    '''创建实体关联边'''
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):#起点节点，终点节点，边，关系类型，关系名字
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))#使用###作为不同关系之间分隔的标志
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')#选取前两个关系，因为两个节点之间一般最多两个关系
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)#match语法，p，q分别为标签，rel_type关系类别，rel_name 关系名字
            try:
                self.g.run(query)#执行语句
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return


    '''导出数据'''
    def export_data(self):

        Dishes, \
        Restaurants, \
        Ingredients, \
        Chefs, \
        Cuisines, \
        Flavors, \
        dish_infos, \
        rels_dish_ingredient, \
        rels_dish_restaurant, \
        rels_dish_chef, \
        rels_dish_cuisine, \
        rels_dish_flavor, \
        rels_restaurant_chef = self.read_nodes()

        print(Dishes)

        f_dish = open('dish.txt', 'w+')
        print(1)
        f_restaurant = open('restaurant.txt', 'w+')
        f_ingredient = open('ingredient.txt', 'w+')
        f_chef = open('chef.txt', 'w+')
        f_cuisine = open('cuisine.txt', 'w+')
        f_flavor = open('flavor.txt', 'w+')

        f_dish.write('\n'.join(list(Dishes)))
        print(2)
        f_restaurant.write('\n'.join(list(Restaurants)))
        f_ingredient.write('\n'.join(list(Ingredients)))
        f_chef.write('\n'.join(list(Chefs)))
        f_cuisine.write('\n'.join(list(Cuisines)))
        f_flavor.write('\n'.join(list(Flavors)))

        f_dish.close()
        print(3)
        f_restaurant.close()
        f_ingredient.close()
        f_chef.close()
        f_cuisine.close()
        f_flavor.close()

        return


if __name__ == '__main__':
    handler = FoodGraph()

    print("step1:导入图谱节点中")
    handler.create_graphnodes() #创建节点

    print("step2:导入图谱边中")
    handler.create_graphrels() # 创建关系

    print("step3:导出数据中")
    handler.export_data()




