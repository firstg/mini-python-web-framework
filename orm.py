#!/usr/bin/python  
#coding :utf-8

import MySQLdb
'''
reference:QuickORM 1 https://github.com/2shou/QuickORM/blob/master/data_handler.py
                   2 https://segmentfault.com/a/1190000002475001
          metaclass  http://blog.jobbole.com/21351/
１　超类
4　没写mysql 接口
参考廖雪峰老师的web框架
class User(Model):

    __tablename__='article'
    
    id=Field('id','int',1)
    title=Field('title','varchar(100)',2)
    content=Field('content','text',3)
    date=Field('date','date',4)
第三个参数是无奈之举 我在metaclass 操作Model attrs的时候，Field对象并不按顺序排列
model子类生成sql语句，Model子类不按照Field创建顺序排列 我在数据库插入的时候就
    （
    写到这里的时候，我想到了 

    create_table 函数创建表 并不按照顺序创建 所以创建完后会是这样
    CREATE TABLE IF NOT EXISTS table_name(
         title varchar(100),
        title varchar(100),
        content text,
        date,date，
        id, int
        );
    insert的时候，我用**kw参数依次匹配insert字典参数的键和创建表的Model子类中的Field实例
    的键，这样就不用排序了
    ）

大概sttrs是dict的缘故，我获取Field类中的第三个参数以{number:field instance }方式组合
dict 按照键值排序了
class User(Model):

    __tablename__='article'
    
    id=IntegerField('id')
    title=StringField('title')
    content=TextField('content')
    date=DateField('date')

还可以将Field 作为base_class实现IntegerFiled等数据类型域类 这样书写就接近django了
orm模型 语句基本功能已经实现 
'''
class Field(object):
    def __init__(self,var,data_type,num,*kw):
        self.var=var
        self.data_type=data_type
        self.num=kw

    #def __str__ : return values ..print instance

    def __str__(self):
        return "<%s:%s>"%(self.var,self.data_type)
class ModelMetaclass(type):
    def __new__(cls,name,bases,attrs):
        if name=='Model':  
            return type.__new__(cls,name,bases,attrs)
        print 'found model %s'% name
        mapping={}
        i=1
        for k,v in attrs.items():   
            if isinstance(v,Field):
                mapping[v.num]=v
                attrs.pop(k) 
        #for k in mapping.keys():
            #attrs.pop(k)   
        attrs['__mapping__']=mapping
        return type.__new__(cls,name,bases,attrs)
class Model(object):
    __metaclass__=ModelMetaclass
    __tablename__=None

    def __init__(self,*kw,**kws):
        super(Model,self).__init__(*kw,**kws)

    def __getattr__(self,key):
        return self[key]

    def __setattr__(self,key,value):
        self[key]=value

    def create_table(self):
        
        fields=[]
        for  k ,v in self.__mapping__.items():
            text=v.var+' '+v.data_type+','
            fields.append(text)
        last=fields[-1]
        del fields[-1]
        fields.append(last[:-1])    
        sql='CREATE TABLE  %s(%s);'%(self.__tablename__,''.join(fields))
        return self.__tablename__,sql
    def insert(self,**kws):
        fields=[]
        for  k ,v in self.__mapping__.items():
           fields.append(str(kws.get(v.var)))
        sql="insert into %s values(%s);"%(self.__tablename__,','.join(fields))
        print sql
    def update(self,**kws):
        fields=[]
        for k,v in kws.items():
            text='%s=%s'%(k,v)
            fields.append(text)
        sql="update %s set %s;"%(self.__tablename__,''.join(fields))
        print sql
    def select(self):
        pass

class DataBase(object):
    @classmethod
    def connect(cls,**db_config):
        cls.con=MySQLdb.connect(
            host=db_config.get('host','localhost'),
            port=int(db_config.get('port',3306)),
            user=db_config.get('user','root'),
            passwd=db_config.get('passwd',None),
            db=db_config.get('database',None),
            charset=db_config.get('charset','utf-8')
            )
    @classmethod
    def get_conn(cls):
        if not cls.conn or not cls.conn.open:
            cls.connect(**cls.db_config)
        try:
            cls.conn.ping()
        except MySQLdb.OperationalError:
            cls.connect(**cls.db_config)
        return cls.conn
    @classmethod
    def execute(cls,*args):
        cursor=cls.get_conn().cursor()
        cursor.execute(*args)
        return cursor

class User(Model):

    __tablename__='article'
    
    id=Field('id','int',1)
    title=Field('title','varchar(100)',2)
    content=Field('content','text',3)
    date=Field('date','date',4)

#create table
'''
CREATE TABLE IF NOT EXISTS table_name(
    id, int,
    title varchar(100),
    content text,
    date,date
    );
''' 
u=User()
table ,sql=u.create_table()

u.insert(id=1,title='title',content='this my first blog ',date="16:55")
u.update(id=2)
#print table
#print sql
