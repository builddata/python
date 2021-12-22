# -*- coding: utf-8 -*-
"""
python_函数用法

"""
import pandas as pd
import numpoy as np

import os
dir_name = './'
os.listdir(dir_name) #获取目录下文件名
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', 1000)

# 通过enumerate函数处理列表之后再遍历可以同时获得元素索引和值
list1=['a','d','c']
for index, elem in enumerate(list1):
    print(index, elem)

f = [x + y for x in 'ABCDE' for y in '1234567']
f = [i*2 for i in [3,6,8] if i>4]
f = (x for x in range(1, 10)) #通过生成器可以获取到数据但它不占用额外的空间存储数据
f = {num: num ** 2 for num in range(1, 10)}
prices = {'AAPL': 191.88,'IBM': 149.24,'ORCL': 48.44}
prices2 = {key: value for key, value in prices.items() if value > 100}
list1 = ['name', 'age', 'gender']
list2 = ['Tom', 20, 'man']
dict1 = {list1[i]: list2[i] for i in range(len(list1))}  #下标索引赋值

classCount={}
classCount['a'] = classCount.get('a', 0) + 1
classCount #Out[833]: {'a': 1}

import itertools
itertools.permutations('ABCD')# 产生ABCD的全排列
itertools.combinations('ABCDE', 3)  # 产生ABCDE的五选三组合
itertools.product('ABCD', '123') # 产生ABCD和123的笛卡尔积

from collections import Counter
words = ['look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes', 'eyes']
counter = Counter(words)
print(counter.most_common(3))
mystr = "hello world and itcast and itheima and Python"       #count
print(mystr.count('and')) #3
print(mystr.count('and', 0, 20))#1

import pickle
data={'a':[1,2,3],'b':( 'string','abc')}                       #pickle
Pic=open('testdata.pkl','wb')
pickle.dump(data,Pic)
Pic.close()
Pic=open(r'c:\python\testdata.pkl','rb')
Data=pickle.load(Pic)

sumary = lambda x, y: x + y
print(sumary(10, 20))  # 30                                   #lambda
func = lambda *args: sum(args)
print(func(1, 2, 3, 4, 5))  # 15

odd = lambda x: x % 2 == 1
templist = filter(odd, [1, 2, 3, 4, 5, 6, 7, 8, 9])               #filter
print(list(templist))  # [1, 3, 5, 7, 9]
m2 = map(lambda x, y: x + y, [1, 3, 5, 7, 9], [2, 4, 6, 8, 10])
print(list(m2))  # [3, 7, 11, 15, 19]

d= {'a': 1, 'c': 3, 'b': 2} 
d_order = sorted(d.items(), key=lambda x: x[1], reverse=False)  # sorted按照值排序
print(d_order)   #[('a', 1), ('b', 2), ('c', 3)]

arr=pd.Series([3,2,1,4,5])
arr.where(arr > 1, 10)
print (arr)# [3,2,10,4,5]
data[(np.abs(data)>3).any(1)]  #选出含有“超过3或-3的”行

arr=pd.Series([3,2,1,4,5])                             #map，apply
arr.map('I am a {}'.format) 
arr.apply(lambda x, value: x - value, args=(5, ))
print (arr)# [-2,-3,-4,-1,0] 
arr.nlargest(3)   #[5,4,3]

arr=np.arange(12).reshape((3,4))
arr.ravel()  arr.ravel('F')  #数组扁平化
np.concatenate([arr1,arr2],axis=0)
np.vstack((arr1,arr2))    np.hstack((arr1,arr2))   #数组的合并

df.groupby('销售区域').销售额.agg(['sum', 'max', 'min']) #使用agg方法并指定多个聚合函数
df.groupby('销售区域')[['销售额', '销售数量']].agg({
    '销售额': 'mean', '销售数量': ['max', 'min']})  #对多个列使用不同的聚合函数

pd.pivot_table(df, index='销售区域', values='销售额', aggfunc='sum') #数据透视表

arr = "this is string example....wow!!! this is really string"    #replace
print (arr.replace("is", "was"))
t1 = ('aa', 'b', 'cc', 'ddd')
print('_'.join(t1))  #aa_b_cc_ddd
mystr = "hello world and itcast and itheima and Python"
print(mystr.index('and'))                       #查找索引位置也可以用find# 12
s1 = {10, 20}
s1.add(100) #update()
s1.remove(10) #s1.discard(10)不会报错

df.PB.rolling(1000).quantile(0.25)#   median()




