# -*- coding: utf-8 -*-
"""
pymysql_增加删除数据
ssh-keygen -t rsa -C "youremail@example.com" 生成新的rsa密钥
git:https://blog.csdn.net/qq_36667170/article/details/79094257
新建一个仓库（ Repository）https://blog.csdn.net/jojowei/article/details/89008657
git clone https://github.com/builddata/python.git(SSH地址)
cd python
git init
git add .(提交所有文件)
git add setting.py （更新所有文件）git add * （更新所有文件）
git commit -m “更新说明”   
git push

git 速度慢：
# Github
# Github
140.82.113.3 github.com
199.232.69.194 github.global.ssl.fastly.net
185.199.108.153 assets-cdn.github.com
185.199.109.153 assets-cdn.github.com
185.199.110.153 assets-cdn.github.com
185.199.111.153 assets-cdn.github.com
cmd：ipconfig/flushdns

sqladmin -u用户名 -p旧密码 password 新密码 
导出sql：mysql -u username -p -D dbname < filename.sql

create database <数据库名>；
查看当前使用的数据库： select database();
建表：
create table MyClass(id int(4) not null primary key auto_increment,
name char(20) not null,
sex int(4) not null default '0',
degree double(16,2));

插入数据：insert into <表名> [( <字段名1>[,..<字段名n > ])] values ( 值1 )[, ( 值n )]

查看表 MyClass 中前2行数据：select * from MyClass order by id limit 0,2;

删除：delete from 表名 where 表达式

清空表：delete from MYTABLE;

修改：update 表名 set 字段=新值,… where 条件

在表中增加字段：alter table 表名 add字段 类型 其他;
alter table dbname add column userid int(11) not null primary key auto_increment;

更改表名：rename table 原表名 to 新表名;

mysql数据库的授权：grant select,insert,delete,create,drop
　　 on *.* (或test.*/user.*/. 数据库)
　　 to 用户名@localhost
　　 identified by '密码'；
语句执行顺序：from join on where group by avg,sum.... having select distinct order by limit 
"""

import time
import pymysql
class SQL_EXE():
    def __init__(self): 
              
        self.conn = pymysql.connect(host="localhost",user="root",password="sunboy",
                                    database="test1",charset="utf8")
        self.cursor = self.conn.cursor()

    def exeQuery(self,sql=None):  #查询操作
        self.cursor.execute(sql)            
        res = self.cursor.fetchall()  
        return res

    def exeCUD(self,sql=None):   #删除、更新、新增操作
        self.cursor.execute(sql)    
        self.conn.commit()      
        print("执行完毕...")

    def exeClose(self):     #关闭游标和连接
        self.cursor.close()
        self.conn.close()
        
if __name__=='__main__':
    
    demo = SQL_EXE()    
    table='testa'                               
    res = demo.exeQuery(sql=f"select * from {table} limit 2")    #执行查询操作
    print(res) 
    # demo.exeCUD(sql=f"insert into {table}  values ('ann',20,'厦门',8000)") #插入数据
    # demo.exeCUD(sql=f"UPDATE {table} SET name ='niubia' where salary>5000") #更新数据
    # demo.exeCUD(sql=f"delete from {table} where age>40")     #删除数据
    # demo.exeCUD(sql=f"drop table {table}")       #删除表
    demo.exeClose()
   