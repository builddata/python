# -*- coding: utf-8 -*-
"""
自定义函数

"""
import line_profiler
def prime_num(max_num):
    for num in range(2, max_num):
        if num < 2:
            pass
        elif num == 2:
            pass
        else:
            for i in range(2, num):
                if num % i == 0:
                    break
            else:
                pass


profile = line_profiler.LineProfiler(prime_num)  # 把函数传递到性能分析器
profile.enable()  # 开始分析
prime_num(3000)
profile.disable()  # 停止分析
profile.print_stats()
#---------------------------------------------------------------------------------------

def recursion(n):#递归函数，一般默认递归长度在1000左右，sys.setrecursionlimit(100000) #括号中的值为递归深度
    v = n//2 # 地板除，保留整数
    print(v) # 每次求商，输出商的值
    if v==0:
        ''' 当商为0时，停止，返回Done'''
        return 'Done'
    v = recursion(v) # 递归调用，函数内自己调用自己
recursion(10) # 函数调用
#---------------------------------------------------------------------------------------
def apply_to_list(fun, some_list):#传入函数作为参数
    return fun(some_list)

lst = [1, 2, 3, 4, 5]
print(apply_to_list(sum, lst))
#---------------------------------------------------------------------------------------
def libs(n):                    #yield生成器
    a = 0
    b = 1
    while True:
        a, b = b, a + b
        if a > n:
            return
        yield a
#---------------------------------------------------------------------------------------
def attempt_float(x):
    try:
        return float(x)
    except:
        return x


f=open(path,'w')
try:
    write_to_file(f)
except:
    print ('failed')
else:
    print ('succeeded')
finally:
    f.close()
#----------------------------------------------------------------------------------
from functools import wraps
from random import random
from time import sleep

#python装饰器本质上就是一个函数，它可以让其他函数在不需要做任何代码变动的前提下增加额外的功能，
#装饰器的返回值也是一个函数对象


import time

def decorator(func):
    def wrapper(a, b):#wrapper(*args, **kwargs)
        start_time = time.time()
        func(a,b)
        end_time = time.time()
        print(end_time - start_time)
    return wrapper

@decorator  #@decorator这个语法相当于 执行 func = decorator(func)，func 就被赋值为wrapper
def func(a,b): #，虽然我们在程序显式调用的是 func() 函数，但其实执行的是装饰器嵌套的 wrapper() 函数
    time.sleep(0.8)
    v=a*b
    print (v)

func(5,4) # 函数调用
# 输出：0.800644397735595

def log(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator

@log('execute')
def now():
    print('2015-3-25')
>>> now()
execute now():
2015-3-25
#---------------------------------------------------------------------------------------
#让 一个类发挥装饰器的作用
class logit(object):
    def __init__(self, logfile='out.log'):
        self.logfile = logfile
 
    def __call__(self, func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            log_string = func.__name__ + " was called"
            print(log_string)
            # 打开logfile并写入
            with open(self.logfile, 'a') as opened_file:
                # 现在将日志打到指定的文件
                opened_file.write(log_string + '\n')
            # 现在，发送一个通知
            self.notify()
            return func(*args, **kwargs)
        return wrapped_function
 
    def notify(self):
        # logit只打日志，不做别的
        pass
@logit()
def myfunc1():
    pass

#给 logit 创建子类，来添加 email 的功能
class email_logit(logit):
    '''
    一个logit的实现版本，可以在函数调用时发送email给管理员
    '''
    def __init__(self, email='admin@myproject.com', *args, **kwargs):
        self.email = email
        super(email_logit, self).__init__(*args, **kwargs)
 
    def notify(self):
        # 发送一封email到self.email
        # 这里就不做实现了
        pass
#---------------------------------------------------------------------------------------    
message = 'hello, world!'
print(message.replace('o', 'O').replace('l', 'L').replace('he', 'HE'))

import re
message = 'hello, world!'
pattern = re.compile('[aeiou]')
print(pattern.sub('#', message))   #h#ll#, w#rld!
