# --------------------------------------------------
# !/usr/bin/python
# -*- coding: utf-8 -*-
# PN: XMLIsALL
# FN: rebuilt
# Author: xiaxu
# DATA: 2022/2/22
# Description:项目重构
# ---------------------------------------------------
from xml.sax.handler import ContentHandler
from xml.sax import parse
import os


class Dispatcher:
    def dispatch(self,prefix,name,attrs = None):
        mname = prefix +name.capitalize()
        dname = 'default' + prefix.capitalize() #默认处理程序，相当于原文写入
        method = getattr(self,mname,None)
        if callable(method):args = () #寻找合适的方法
        else:
            method = getattr(self,dname,None)
            args = name,  #这里要注意，赋值的是元组
        if prefix == 'start': args += attrs, #这里也必须是元组，元组到元组，否则则会报错
        # can only concatenate tuple (not "AttributesImpl") to tuple
        if callable(method):method(*args)

    def startElement(self,name,attrs):
        self.dispatch("start",name,attrs)

    def endElement(self,name):
        self.dispatch("end",name)


class WebsiteConstructor(Dispatcher,ContentHandler):
    passthrough = False
    def __init__(self,directory):
        self.directory = [directory]
        self.ensure_directory()

    def ensure_directory(self):  #保证目录存在
        path = os.path.join(*self.directory)
        os.makedirs(path,exist_ok = True)

    def startPage(self,attrs): #开始页面
        filename = os.path.join(*self.directory+[attrs['name']+'.html'])
        self.out = open(filename,'w')
        self.writeHeader(attrs['title'])
        self.passthrough = True

    def writeHeader(self,title): #头信息写入
        self.out.write('<html>\n  <head>\n    <title>')
        self.out.write(title)
        self.out.write('</title>\n  </head>\n  <body>\n')

    def endPage(self): #结束页面
        self.passthrough = False
        self.writeFooter()
        self.out.close()

    def writeFooter(self): #尾信息写入
        self.out.write('</body>\n</html>\n')

    def characters(self, content):
        if self.passthrough:
            self.out.write(content)

    def defaultStart(self,name,attrs):
        if self.passthrough:
            self.out.write('<' + name)
            for key, val in attrs.items():
                self.out.write(' {}="{}"'.format(key, val))
            self.out.write('>')

    def defaultEnd(self,name):
        if self.passthrough:
            self.out.write('</{}>'.format(name))

    def startDrictory(self,attrs): #目录处理程序
        self.directory.append(attrs['name'])
        self.ensure_directory()

    def endDrictory(self):
        self.directory.pop()

parse('website.xml',WebsiteConstructor('public_html'))



