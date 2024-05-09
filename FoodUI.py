#!/usr/bin/env python
# coding=utf-8
# programmer:Jarsore,05/03/2024

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from foodQAsystem_graph import *

class MyWindow(QWidget):

    def __init__(self):
        super(MyWindow, self).__init__()
        self.background_path = r"D:\Documents\QAFoodKG\bkg.png"
        self.init_UI()


    def init_UI(self):
        # 设置窗口大小
        self.setFixedSize(680, 600)
        self.setBackground()
        # 创建一个只读文本框【回复】
        self.text_edit_reply = QTextEdit(self)
        self.text_edit_reply.setReadOnly(True)
        self.text_edit_reply.setText("sgbdasihdbuaiks")
        self.text_edit_reply.setGeometry(QRect(100,100,300,70))#x,y,width,height

        # 创建一个文本输入框【输入】
        self.text_eidt_query = QTextEdit(self)
        self.text_eidt_query.setGeometry(QRect(100,180,300,70))
        self.text_eidt_query.setPlaceholderText("请输入")

        # 创建并设置发送按钮
        self.btn_send = QPushButton("Send", self)
        self.btn_send.setGeometry(QRect(300, 280, 100, 40))  # 设置位置和大小
        self.btn_send.clicked.connect(self.on_send_click)  # 连接点击信号
        # 显示窗口
        self.show()
    def setBackground(self):
        self.setStyleSheet(f"background-image: url({self.background_path});")
    def on_send_click(self):
        # 这里可以定义点击发送按钮时的行为
        print("Send button clicked")
        text_query = self.text_eidt_query.toPlainText()
        print("text_query=",text_query," type=",type(text_query))
        # self.text_eidt_query.clear()
        handler = FoodQASystemGraph()
        answer = handler.chat_main(text_query)
        self.text_edit_reply.clear()
        self.text_edit_reply.setText(answer)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWindow()
    # 设置窗口标题
    w.setWindowTitle("美食问答系统")
    # 展示窗口
    w.show()
    # 程序进入循环等待状态
    app.exec_()