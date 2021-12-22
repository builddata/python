import pandas as pd
import numpy as np
from pandas import DataFrame, Series
import requests
import json
import urllib
import random
from sqlalchemy import create_engine
import re
from bs4 import BeautifulSoup

headers = {
    'Host': 'win.hibor.com.cn',
    'Connection': 'keep-alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
}

i=0

url = 'https://win.hibor.com.cn/baogao/Docinfo/ListIndexSearchPage?abc=qRuMnNoNmMmMmNqOqQvNzR&def=tRmMpNmNjMnMnNlOsQnNbRpOmRuOnMtNNZqMtO&xyz=tRoMmNvNoMnMoN&vidd=2&keyy=GYTJJGHJ&op=0&page=0&bigType=%E7%A0%94%E7%A9%B6%E6%8A%A5%E5%91%8A&miniType=%E5%85%AC%E5%8F%B8%E8%B0%83%E7%A0%94&hiddocType=1&hidthes2=0&hidthes3=0&jichuban=&docType=1&thes2=0&time=25&selquans=&selauthor=0&seldocpages=0&selhangye=%E5%85%A8%E9%83%A8&selpingji=0&selfiletype=&area=DocTitle&key='
url.replace(re.findall('page=.*?&', url)[0], 'page=%d&' % i)


data = requests.get(url=url,headers=headers).text  #直接.text就行,不用.content再解码成utf-8

soup = BeautifulSoup(data,'lxml') #解析成html格式

#观察发现所有的数据都在<tr></tr>里面,除了最后一个<tr></tr>不是
#soup.find_all找出所有<tr></tr>组成一个列表
soup_list = soup.find_all(name='tr')

#!!注意,除了最后一个数据外,每页本应有50个数据,但此处会有100个数据,
#前50个和后50个内容是一样的,但格式不一样,这里取前50个就行了(后50个对于'今天'这样的提法没有准确的日期)
soup_list = soup_list[:50]

df = pd.DataFrame({'title':[],'date':[],'time':[],'hot':[],'class':[],'level':[],'author_1':[],'author_2':[],'page':[]})

for s in range(len(soup_list)):

    #标题
    #标题在name='a'的[0]里,repr转为字符串,split切割定位,其他的以此类推
    title = repr(soup_list[s].find_all(name='a')[0]).split('title="')[1].split('">')[0]

    #日期和时间
    date_time = repr(soup_list[s].find_all(name='span')[1]).split('title="')[1].split('">')[0]
    date = date_time.split(' ')[0]
    time = date_time.split(' ')[1]
    date = int(date[:4]+date[5:7]+date[8:10])

    #热度
    hot = int(repr(soup_list[s].find_all(name='span')[2]).split('style="width: ')[1].split('px">')[0])

    #分类
    #这里中间会有几个span,建议之后的span从后往前数
    class_ = repr(soup_list[s].find_all(name='span')[3]).split('title="')[1].split('">')[0] 

    #评级
    level = repr(soup_list[s].find_all(name='span')[-3]).split('title="')[1].split('">')[0].replace(' ','').replace('\r','').replace('\n','')

    #作者
    author = repr(soup_list[s].find_all(name='span')[-2]).split('target="_blank">')[1].split('</a>')[0] 

    #把<i class="user-msg-i" id="叶寅_平安证券_1"></i>替换成逗号
    author_1 = re.sub('<i(.+?)</i>', '，', author).replace(' ','').replace('\r','').replace('\n','')
    #如果最后一位是逗号,去除
    if author_1[-1] == '，': 
        author_1 = author_1[:-1]

    #把所有获奖的找出来用逗号分隔
    author_2 = ''
    for n in re.findall('<i(.+?)</i>',author):
        author_2 = author_2 + n.split('id="')[1].split('">')[0] + '，'
    #如果最后一位是逗号,去除
    try: #如果无数据就跳过
        if author_2[-1] == '，': 
            author_2 = author_2[:-1]
    except:
        pass


    #页数
    page = int(repr(soup_list[s].find_all(name='span')[-1]).split('class="list-page">')[1].split('</span>')[0].replace(' ','').replace('\r','').replace('\n','').replace('页',''))

    #创建单数据df
    df_ = pd.DataFrame({'title':[title],'date':[date],'time':[time],'hot':[hot],'class':[class_],'level':[level],'author_1':[author_1],'author_2':[author_2],'page':[page]})

    #添加到总df
    df = df.append(df_)
    
df = df.reset_index(drop=True)