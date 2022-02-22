from xml.sax.handler import ContentHandler
from xml.sax import parse
import os

class Dispatcher:

    def dispatch(self, prefix, name, attrs=None): #分派器，将事件分派给子定义的事件处理程序
        mname = prefix + name.capitalize() #对于需要处理的，如html的头尾，文件的打开和关闭，首字符大写
        dname = 'default' + prefix.capitalize() #默认处理程序，相当于原文写入
        method = getattr(self, mname, None)
        if callable(method): args = () #
        else:
            method = getattr(self, dname, None) #使用默认方法，将标签作为参数，因为需要传递
            args = name,
        if prefix == 'start': args += attrs, #开始属性需要传递作为名称的属性
        if callable(method): method(*args)

    def startElement(self, name, attrs):
        self.dispatch('start', name, attrs) #这里使用了分派器来实现不同方法的分派

    def endElement(self, name):
        self.dispatch('end', name)

class WebsiteConstructor(Dispatcher, ContentHandler):

    passthrough = False

    def __init__(self, directory): #将当前目录路径存储，以便后面创建
        self.directory = [directory]
        self.ensureDirectory()

    def ensureDirectory(self):  #支持目录，为了使点击超链接时能够响应
        path = os.path.join(*self.directory) #使用*进行了参数拆分，再使用join合并为路径
        os.makedirs(path, exist_ok=True) #为了避免目录存在时引发异常

    def characters(self, chars):
        if self.passthrough: self.out.write(chars)

    def defaultStart(self, name, attrs):
        if self.passthrough: #对xml不做任何处理，原文写入
            self.out.write('<' + name)
            for key, val in attrs.items():
                self.out.write(' {}="{}"'.format(key, val))
            self.out.write('>')

    def defaultEnd(self, name):  #原文写入结束标签
        if self.passthrough:
            self.out.write('</{}>'.format(name))

    def startDirectory(self, attrs):
        self.directory.append(attrs['name']) #将directory的目录添加为子目录
        self.ensureDirectory()

    def endDirectory(self):
        self.directory.pop()

    def startPage(self, attrs):
        filename = os.path.join(*self.directory + [attrs['name'] + '.html'])
        self.out = open(filename, 'w')
        self.writeHeader(attrs['title'])
        self.passthrough = True

    def endPage(self):
        self.passthrough = False
        self.writeFooter()
        self.out.close()

    def writeHeader(self, title): #首部写入文件
        self.out.write('<html>\n  <head>\n    <title>')
        self.out.write(title)
        self.out.write('</title>\n  </head>\n  <body>\n')

    def writeFooter(self): #尾部写入文件
        self.out.write('\n  </body>\n</html>\n')

parse('website.xml', WebsiteConstructor('public_html'))