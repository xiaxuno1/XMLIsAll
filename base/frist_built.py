# --------------------------------------------------
# !/usr/bin/python
# -*- coding: utf-8 -*-
# PN: XMLIsALL
# FN: frist_built
# Author: xiaxu
# DATA: 2022/2/21
# Description:初次实现，xml创建html文件
# ---------------------------------------------------
from xml.sax.handler import ContentHandler
from xml.sax import parse

class PageMaker(ContentHandler):
    passthrough = False
    def startElement(self, name, attrs):
        if name == "page":
            self.passthrough = True
            self.out = open(attrs["name"]+"html","w") #根据标签的名字属性确定文件名
            self.out.write("<html><head>\n")  #文件头
            self.out.write("<title>{}</title>\n".format(attrs["title"])) #文件的标题
            self.out.write("</head><body>\n")
        elif self.passthrough:#这部分原样写入html
            self.out.write("<"+name)
            for key,val in attrs.items():
                self.out.write('{}="{}"'.format(key,val)) #属性和属性值原样写入
            self.out.write(">")
    def endElement(self, name):
        if name == "page":
            self.passthrough = False
            self.out.write("\n</body></html>\n")
            self.out.close()
    def characters(self, content):
        if self.passthrough:
            self.out.write(content)
parse('website.xml',PageMaker())

