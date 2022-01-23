# -*- coding: utf-8 -*-
"""
类:类和类之间的关系有三种：is-a继承、has-a关联和use-a依赖关系
pip 国内
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
"""
class people:
    # 定义基本属性
    name = ''
    age = 0
    # 定义私有属性,私有属性在类外部无法直接进行访问
    __weight = 0
    # 定义构造方法
    def __init__(self, n, a, w):
        self.name = n
        self.age = a
        self.__weight = w
    def speak(self):
        print("%s 说: 我 %d 岁。" % (self.name, self.age))
        
class student(people):
    grade = ''
    def __init__(self, n, a, w, g): 
        super.__init__(n, a, w)
        self.grade = g
    # 覆写父类的方法
    def speak(self):
        print("%s 说: 我 %d 岁了，我在读 %d 年级" % (self.name, self.age, self.grade))
#--------------------------------------------------------------------------------------
class Person(object):
    # 限定Person对象只能绑定_name, _age和_gender属性
    __slots__ = ('_name', '_age', '_gender')
    def __init__(self, name, age):
        self._name = name
        self._age = age

    # 访问器 - getter方法
    @property
    def name(self):
        return self._name
    # 访问器 - getter方法
    @property
    def age(self):
        return self._age
    # 修改器 - setter方法
    @age.setter
    def age(self, age):
        self._age = age
    def play(self):
        if self._age <= 16:
            print('%s正在玩飞行棋.' % self._name)
        else:
            print('%s正在玩斗地主.' % self._name)
def main():
    person = Person('王大锤', 12)
    person.play()
    person.age = 22
    person.play()
    # person.name = '白元芳'  # AttributeError: can't set attribute

if __name__ == '__main__':
    main()
    
#----------------------------------
#但是如果外部代码要获取name和score怎么办？可以给Student类增加get_name和get_score这样的方法：    

class Student(object):
    def __init__(self, name, score):
        self.__name = name
        self.__score = score
    def get_name(self):
        return self.__name

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value
#----------------------------------------------------------------------------------------
#当我们调用这个经过子类重写的方法时，不同的子类对象会表现出不同的行为，这个就是多态（poly-morphism）
from abc import ABCMeta, abstractmethod
class Pet(object, metaclass=ABCMeta):
    """宠物"""
    def __init__(self, nickname):
        self._nickname = nickname
    @abstractmethod
    def make_voice(self):
        """发出声音"""
        pass
class Dog(Pet):
    """狗"""
    def make_voice(self):
        print('%s: 汪汪汪...' % self._nickname)
class Cat(Pet):
    """猫"""
    def make_voice(self):
        print('%s: 喵...喵...' % self._nickname)
def main():
    pets = [Dog('旺财'), Cat('凯蒂'), Dog('大黄')]
    for pet in pets:
        pet.make_voice()

if __name__ == '__main__':
    main()
#----------------------------------------------------------------------------------------
#Dict 是 Python 中的 K-V 容器，但是如果试图从 Dict 中获取一个不存在的 key 则会抛出 KeyError 异常，
#这在很多时候非常不方便
class MyDict(dict):            #或者 使用dic.get('a','default')
    def __init__(self):
        self.a = None
    def __missing__(self,key):
        self[key]='default'
        return "default"
#b['a'] Out[783]: 'default'
#b['a']=0 
#b['a'] Out[787]: 0

class Student(dict):
    def __init__(self):
        self.name=None
        self.score=None
        self.profit=None
        self.initial_capital=None
        
    def get_account(self):
        """
        account details
        """
        account = {}
        account['initial_capital'] = self.initial_capital
        account['cum_profit'] = self.profit
        return account
a.initial_capital=99999
a.profit=88
a.get_account()
Out[818]: {'initial_capital': 99999, 'cum_profit': 88}
#-----------------------------------------------------------------------------------
from math import sqrt
class Triangle(object):

    def __init__(self, a, b, c):
        self._a = a
        self._b = b
        self._c = c

    @staticmethod   #该方法不强制要求传递参数
    def is_valid(a, b, c):
        return a + b > c and b + c > a and a + c > b

    def perimeter(self):
        return self._a + self._b + self._c

    def area(self):
        half = self.perimeter() / 2
        return sqrt(half * (half - self._a) *
                    (half - self._b) * (half - self._c))


def main():
    a, b, c = 3, 4, 5
    # 静态方法和类方法都是通过给类发消息来调用的
    if Triangle.is_valid(a, b, c): # # 静态方法无需实例化
        t = Triangle(a, b, c)
        print(t.perimeter())
        # 也可以通过给类发消息来调用对象方法但是要传入接收消息的对象作为参数
        print(Triangle.perimeter(t))
        print(t.area())
        # print(Triangle.area(t))
    else:
        print('无法构成三角形.')
if __name__ == '__main__':
    main()
#---------------------------------------------------------------------------------------
#默认情况下，__repr__() 会返回和调用者有关的 “类名+object at+内存地址”信息。
#当然，我们还可以通过在类中重写这个方法，从而实现当输出实例化对象时，输出我们想要的信息。
#__str__ 的返回结果可读性强。也就是说，__str__ 的意义是得到便于人们阅读的信息，
#就像上面的 '2019-10-20 20:59:47.003003' 一样。

#__repr__ 的返回结果应更准确。怎么说，__repr__ 存在的目的在于调试，便于开发者使用。
#将 __repr__ 返回的方式直接复制到命令行上，是可以直接执行的

class CLanguage:
    def __init__(self):
        self.name = "C语言中文网"
        self.add = "http://c.biancheng.net"
    def __repr__(self):# def __str__(self):
        return "CLanguage[name="+ self.name +",add=" + self.add +"]"
clangs = CLanguage()
print(clangs)   #CLanguage[name=C语言中文网,add=http://c.biancheng.net]
#------------------------------------------------------------------------------------------
#__call__()。该方法的功能类似于在类中重载 () 运算符，使得类实例对象可以像调用普通函数那样，
#以“对象名()”的形式使用
class CLanguage:
    # 定义__call__方法
    def __call__(self,name,add):
        print("调用__call__()方法",name,add)

clangs = CLanguage()
clangs("C语言中文网","http://c.biancheng.net")

#--------------------------------------------------------
#一个类想被用于for ... in循环
#要表现得像list那样按照下标取出元素，需要实现__getitem__()方法：
class Fib(object):
    def __init__(self):
        self.a, self.b = 0, 1 # 初始化两个计数器a，b

    def __iter__(self):
        return self # 实例本身就是迭代对象，故返回自己

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b # 计算下一个值
        if self.a > 100000: # 退出循环的条件
            raise StopIteration()
        return self.a # 返回下一个值
    def __getitem__(self, n):
        a, b = 1, 1
        for x in range(n):
            a, b = b, a + b
        return a
    
for n in Fib():
     print(n)

#---------------------------------------------------------
#正常情况下，我们都用class Xxx...来定义类，但是，type()函数也允许我们动态创建出类来
def fn(self, name='world'): # 先定义函数
     print('Hello, %s.' % name)

>>> Hello = type('Hello', (object,), dict(hello=fn)) # 创建Hello class
>>> h = Hello()
>>> h.hello()
Hello, world.
#1.class的名称；
#2.继承的父类集合，注意Python支持多重继承，如果只有一个父类，别忘了tuple的单元素写法；
#3.class的方法名称与函数绑定，这里我们把函数fn绑定到方法名hello上。














