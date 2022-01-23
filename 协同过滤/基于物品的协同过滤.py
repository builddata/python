# -*- coding: utf-8 -*-
"""
基于物品的协同过滤

基于用户的协同过滤算法(UserCF): 给用户推荐和他兴趣相似的其他用户喜欢的产品:
    即当一个用户A需要个性化推荐的时候，我们可以先找到和他有相似兴趣的其他用户，
    然后把那些用户喜欢的，而用户A没有听说过的物品推荐给A。
    利用用户相似度和相似用户的评价加权平均获得用户的评价预测
基于物品的协同过滤算法(ItemCF): 给用户推荐和他之前喜欢的物品相似的物品

基于用户的协同过滤需要在线找用户和用户之间的相似度关系，计算复杂度肯定会比基于基于项目的协同过滤高。
但是可以帮助用户找到新类别的有惊喜的物品。而基于项目的协同过滤，由于考虑的物品的相似性一段时间不会改变，
因此可以很容易的离线计算，准确度一般也可以接受，但是推荐的多样性来说，就很难带给用户惊喜了。
一般对于小型的推荐系统来说，基于项目的协同过滤肯定是主流。但是如果是大型的推荐系统来说，
则可以考虑基于用户的协同过滤


"""

#-*-coding:utf-8-*-  
  
#1.在计算推荐度时，是否需要只考虑相似度排名前k的产品？如果考虑的话，会对排序的结果产生怎么样的影响呢？

#2.借过的产品在模型里不会被推荐。如何兼容复借产品的排序和推荐？

#3.新上线的产品由于取不到历史数据，不会进入模型。如何兼容新上线产品的排序和推荐？
  
import pandas as pd
import numpy as np
import math 
import os
import time
import datetime

# os.chdir(r'f:\zxx\pthon_work\CF')

def loadData():
    #读入movies.dat, rating.dat,tags.dat
    #mnames=['movie_id','title','genres']
    #movies=pd.read_table(r'.\data\movies.dat',sep='::',header=None,names=mnames)

    rnames=['UserID','MovieID','Rating','Timestamp']
    all_ratings=pd.read_csv(r'D:/data_analysis/ml-latest-small/ratings.csv',header=None,names=rnames,nrows=300000)


    return all_ratings

#数据探索：rating
def data_alay(ratings):
   """rating nums10000054, 3, 
   示例 ：    1      122       5  838985046
   col:'UserID','MovieID','Rating','Timestamp'
       """
   #一个用户只对一个电影打分一次
   UR=ratings.groupby([ratings['UserID'],ratings['MovieID']])
   len(UR.size)

#计算每部电影的平均打分,电影数10677
def avgRating(ratings):
    movies_mean=ratings['Rating'].groupby(ratings['MovieID']).mean()#计算所有用户对电影X的平均打分
    movies_id=movies_mean.index
    movies_avg_rating=movies_mean.values
    return movies_id,movies_avg_rating,movies_mean

#计算电影相似度矩阵相，即建立10677*10677矩阵
def calculatePC(ratings):
    movies_id,movies_avg_rating,movies_mean=avgRating(ratings)
    #pc_mat=np.eye(3)#建立电影相似度单位矩阵
    pc_dic={}
    top_movie=len(movies_id)
    for i in range(0,top_movie):
        for j in range(i+1,top_movie):
            movieAID=movies_id[i]
            movieBID=movies_id[j]
            see_moviesA_user=ratings['UserID'][ratings['MovieID']==movieAID]
            see_moviesB_user=ratings['UserID'][ratings['MovieID']==movieBID]
            join_user=np.intersect1d(see_moviesA_user.values,see_moviesB_user.values)#同时给电影A、B评分的用户
            movieA_avg=movies_mean[movieAID]
            movieB_avg=movies_mean[movieBID]
            key1=str(movieAID)+':'+str(movieBID)
            key2=str(movieBID)+':'+str(movieAID)
            value=twoMoviesPC(join_user,movieAID,movieBID,movieA_avg,movieB_avg,ratings)
            pc_dic[key1]=value            
            pc_dic[key2]=value                        
            #pc_mat[i][i+1]=twoMoviesPC(join_user,movieAID,movieBID,movieA_avg,movieB_avg,ratings)
            #print ('---the %s, %d,%d:--movie %s--%s--pc is %f' % (key1,movieAID,movieBID,movieAID,movieBID,pc_dic[key1]))
    return pc_dic

#计算电影A与电影B的相似度，皮尔森相似度=sum(A-A^)*sum(B-B^)/sqrt(sum[(A-A^)*(A-A^)]*sum[(B-B^)*(B-B^)])
def twoMoviesPC(join_user,movieAID,movieBID,movieA_avg,movieB_avg,ratings):
    cent_AB_sum=0.0#相似度分子
    centA_sum=0.0#分母
    centB_sum=0.0#分母
    movieAB_pc=0.0#电影A,B的相似度
    count=0
    for u in range(len(join_user)):
        #print '---------',u
        count=count+1
        ratA=ratings['Rating'][ratings['UserID']==join_user[u]][ratings['MovieID']==movieAID].values[0]#用户给电影A评分
        ratB=ratings['Rating'][ratings['UserID']==join_user[u]][ratings['MovieID']==movieBID].values[0]#用户给电影B评分
        cent_AB=(ratA-movieA_avg)*(ratB-movieB_avg) #去均值中心化
        centA_square=(ratA-movieA_avg)*(ratA-movieA_avg) #去均值平方
        centB_square=(ratB-movieB_avg)*(ratB-movieB_avg)#去均值平方
        cent_AB_sum=cent_AB_sum+cent_AB
        centA_sum=centA_sum+centA_square
        centB_sum=centB_sum+centB_square
    if(centA_sum>0 and centB_sum>0 ):
       movieAB_pc=cent_AB_sum/math.sqrt(centA_sum*centB_sum)
    return movieAB_pc

"""
预测用户U对那些电影感兴趣。分三步，
  1）用户U过去X天看过的电影。
  2）提出用户U已看过的电影，根据用户U过去看过的电影，计算用户U对其他电影的打分.
  3) 拉去打分最高的的电影给用户推荐。
预测用户U对电影C的打分。分三步：（先只做这个）
  1）用户U过去X天看过的电影。
  2）利用加权去中心化公式预测用户U对电影C的打分.

"""
#日期处理： -3天，然后转换为uinxtime
def timePro(last_rat_time,UserU):
    lastDate= datetime.datetime.fromtimestamp(last_rat_time[UserU]) #unix转为日期
    date_sub3=lastDate+datetime.timedelta(days=-3)#减去3天
    unix_sub3=time.mktime(date_sub3.timetuple())#日期转为unix
    return unix_sub3

#取用户最后一次评分前3天评估的电影进行预测
def getHisRat(ratings,last_rat_time,UserUID):
    unix_sub3= timePro(last_rat_time,UserUID)
    UserU_info=ratings[ratings['UserID']==UserUID][ratings['Timestamp']>unix_sub3]
    return UserU_info

#预测用户U对电影C的打分
def hadSeenMovieByUser(UserUID,MovieA,ratings,pc_dic,movies_mean):
    pre_rating=0.0    
    last_rat_time=ratings['Timestamp'].groupby([ratings['UserID']]).max()#获取用户U最近一次评分日期
    UserU_info= getHisRat(ratings,last_rat_time,UserUID)#获取用户U过去看过的电影

    flag=0#表示新电影，用户U是否给电影A打过分
    wmv=0.0#相似度*mv平均打分去均值后之和
    w=0.0#相似度之和
    movie_userU=UserU_info['MovieID'].values#当前用户看过的电影
    if MovieA in movie_userU:
        flag=1
        pre_rating=UserU_info['Rating'][UserU_info['MovieID']==MovieA].values
    else:
        for mv in movie_userU:
            key=str(mv)+':'+str(MovieA)
            rat_U_mv=UserU_info['Rating'][UserU_info['MovieID']==mv][UserU_info['UserID']==UserUID].values#用户U对看过电影mv的打分
            wmv=(wmv+pc_dic[key]*(rat_U_mv-movies_mean[mv]))#相似度*mv平均打分去均值后之和
            w=(w+pc_dic[key])#看过电影与新电影相似度之和
            print (w)
            #print ('---have seen mv %d with new mv %d,%f,%f'%(mv,MovieA,wmv,w))            
            pre_rating=(movies_mean[MovieA]+wmv/w)
    print ('-flag:%d---User:%d rating movie:%d with %f score----' %(flag,UserUID,MovieA,pre_rating))
    return pre_rating,flag

if __name__=='__main__':
    all_ratings=loadData()[1:300000]
    all_ratings.MovieID=all_ratings.MovieID.astype('int')
    all_ratings.Rating=all_ratings.Rating.astype('int')
    all_ratings.Timestamp=all_ratings.Timestamp.astype('int')
    movie_num=100#控制电影数，只针对电影ID在该范围的数据进行计算，否则数据量太大  
   
    ratings=all_ratings[all_ratings['MovieID']<=movie_num]

    movies_id,movies_avg_rating,movies_mean=avgRating(ratings)
    pc_dic=calculatePC(ratings)#电影相似度矩阵
    #预测
    UserUID=10#当前数据集只看过电影4，7，
    MovieA=6    
    pre_rating,flag=hadSeenMovieByUser(UserUID,MovieA,ratings,pc_dic,movies_mean)

    "-----------------测试ID提取------------------"
    #选取UserUID
    ratings.head(10)#从前10行中随机选取一个用户ID,例如：UserID=10
    #查看该用户在当前数据集中看过那些电影，方便选取新电影（防止选择的是用户已经看过的电影）
    ratings[ratings['UserID']==10]#该用户在当前数据集中，只看过电影MovieID in(4，7)，则可选择不是4，7的电影ID进行预测，例如6.
