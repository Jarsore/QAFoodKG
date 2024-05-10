#!/usr/bin/env python
# coding=utf-8
# programmer:Jarsore,05/03/2024

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from foodQAsystem_graph import *
from question_classifier import *
from question_parser import *
from answer_search import *
from PyQt5.QtGui import QPixmap,QPalette
from PyQt5.QtGui import QIcon


class MyWindow(QWidget):

    def __init__(self):
        super(MyWindow, self).__init__()

        self.background_path = r"D:\Documents\QAFoodKG\rice.jpg"

        self.init_UI()


    def init_UI(self):
        # 设置窗口大小
        # self.setFixedSize(680, 600)
        self.setFixedSize(960, 640)
        self.setWindowIcon(QIcon('Logo.ico'))
        self.setBackground()

        # 创建一个文本输入框【输入】
        self.text_eidt_query = QTextEdit(self)
        self.text_eidt_query.setGeometry(QRect(70,100,300,70))
        self.text_eidt_query.setPlaceholderText("用户美食咨询，请输入：")

        # 创建一个只读文本框【回复】
        self.text_edit_reply = QTextEdit(self)
        self.text_edit_reply.setReadOnly(True)
        self.text_edit_reply.setText("兰陵美酒郁金香，玉碗盛来琥珀光")
        self.text_edit_reply.setGeometry(QRect(70,180,300,70))#x,y,width,height

        # 创建一个查询语句显示框
        self.text_edit_cypher = QTextEdit(self)
        self.text_edit_cypher.setReadOnly(True)
        self.text_edit_cypher.setText("查询语句显示")
        self.text_edit_cypher.setGeometry(QRect(10, 580, 700, 50))  # x,y,width,height

        # 创建并设置发送按钮
        self.btn_send = QPushButton("确定", self)
        self.btn_send.setGeometry(QRect(450, 100, 100, 150))  # 设置位置和大小
        self.btn_send.clicked.connect(self.on_send_click)  # 连接点击信号

        # 显示窗口
        self.show()

    def setBackground(self):

        # self.setStyleSheet(f"background-image: url({self.background_path});")

        # # 加载背景图片
        # pixmap = QPixmap(self.background_path)
        # # 设置窗口背景
        # self.setPalette(QPalette(Qt.transparent))
        # self.setAutoFillBackground(False)
        # self.label = QLabel(self)
        # self.label.setPixmap(pixmap)
        # self.label.setAlignment(Qt.AlignCenter)
        # layout = QVBoxLayout()
        # layout.addWidget(self.label)
        # self.setLayout(layout)


        self.setPalette(QPalette(Qt.transparent))  # 设置窗口背景为透明
        self.setAutoFillBackground(False)  # 禁用自动填充背景
        pixmap = QPixmap(self.background_path)
        self.label = QLabel(self)
        self.label.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet('background-color: transparent;')  # 设置标签背景透明
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # 设置布局边距为0
        layout.addWidget(self.label)
        self.setStyleSheet('background-color: transparent;')  # 设置窗口背景透明


    def on_send_click(self):
        # 这里可以定义点击发送按钮时的行为
        print("Send button clicked")
        text_query = self.text_eidt_query.toPlainText()
        print("text_query=",text_query," type=",type(text_query))
        # self.text_eidt_query.clear()



        # 实例化问答系统并获取答案和SQL语句
        handler = FoodQASystemGraph()

        # answer = handler.chat_main(text_query)
        result = handler.chat_main(text_query)


        # 清空并设置查询语句文本框
        self.text_edit_cypher.clear()
        self.text_edit_cypher.setText(str(result['res_sql']))
        # 清空并设置回答文本框
        self.text_edit_reply.clear()
        self.text_edit_reply.setText(str(result['answer']))

        # self.text_edit_reply.clear()
        # self.text_edit_reply.setText(answer)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = MyWindow()
    # 设置窗口标题
    w.setWindowTitle("美食问答系统")
    # 展示窗口
    w.show()
    # 程序进入循环等待状态
    app.exec_()
