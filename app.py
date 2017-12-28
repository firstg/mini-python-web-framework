
import re
'''
reference:1 web app http://www.cnblogs.com/russellluo/p/3338616.html
          2 iterator generator http://python.jobbole.com/81916/
                               http://www.cnblogs.com/jessonluo/p/4732565.html
          3 decorator @        https://www.python.org/dev/peps/pep-0318/
                               http://python.jobbole.com/80956/
１迭代对象　迭代器　生成器　正则re
２还可以用修饰符来获取path_info等等
迭代器　iterator 有__iter__ 方法　返回一个迭代器　有next()方法　　用for来获取临时生成的值
生成器　generator 生成器就是一个特殊的迭代器 有yield关键字的方法为生成器　该函数返回的是一个
迭代器　需要用　for　语句来获取值
for ---in --- 
首先调用被循环的迭代对象的__iter__方法　获取迭代器，然后用获取的迭代器的next()方法　不断获取值,直到next到下一个不存在或极限的值　后，抛出一个Stopiteration异常
for value in iterable:
iterator object=iterable()
   while True:
     try:
      iterator.next()
     except Stopiteation:
      return 
还有很多地方可以共同的地方抽出来作为单独类（简洁）
以前我不明白为什么用迭代器（生成器） 看了他们的实现原理后大概明白了：
就拿生成器函数（yield）举例
    web中传输文件 一部电影几G，我们不可能一次传给接收方 ，因为在传给接收方前函数需要将
    字节码文件一次性读取到内存中 （可能内存不够），
    我们需要一点一点的传： 函数从硬盘中先读很小一部分，传给对面，传完之后，函数就把这部分内存释放，
    然后再接着上次读取的地方再读取一小部分，传给接收方。  如此反复反复 直到读取完。
    整个程序在运行过程中 内存始终是小开支的，就是函数所占的内存 和一部分数据所占的内存
'''
urls = {
        ("/", "index"),
        ("/hello/(.*)", "hello"),
    }
 
class Base_app:

    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response

    def __iter__(self):
        return self
    def __next__(self):
        self.delegate()
    def __iter__(self): 
        result = self.delegate()

        if isinstance(self,basestring):
            return iter(result)
        else:
            return iter(result)
        
    def delegate(self): 

        path = self.environ['PATH_INFO'] 
        for pattern, name in urls:
           
            m = re.match('^' + pattern + '$', path)
            print m
            if m:
                arg = m.groups()
                if hasattr(self, name):
                    func = getattr(self, name)
                    return func(*arg)
            
        return self.notfound()

class app(Base_app):
    
    def index(self):
        status='200 OK'
        headers=[('Content-type', 'text/plain')]
        self.start(status,headers)
        return 'index page'
    def hello(self,name):
        status='200 OK'
        headers=[('Content-type', 'text/plain')]
        self.start(status,headers)
        return 'hello %s'%name
    def notfound(self):
        status = '404 Not Found'
        headers=[('Content-type', 'text/plain')]
        self.start(status,headers)
        return 'no found'    

