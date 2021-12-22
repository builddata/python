# -*- coding: utf-8 -*-
"""
协程异步IO（asyncio）
因为阻塞的协程对象会放弃对 CPU 的占有而不是让 CPU 处于闲置状态，这种方式大大的提升了 CPU 的利用率

event_loop 事件循环：程序开启一个无限的循环，程序员会把一些函数注册到事件循环上。
当满足事件发生的时候，调用相应的协程函数。

coroutine 协程：协程对象，指一个使用async关键字定义的函数，它的调用不会立即执行函数
，而是会返回一个协程对象。协程对象需要注册到事件循环，由事件循环调用。

task 任务：一个协程对象就是一个原生可以挂起的函数，任务则是对协程进一步封装，其中包含任务的各种状态。

future： 代表将来执行或没有执行的任务的结果。它和task上没有本质的区别

async/await 关键字：python3.5 用于定义协程的关键字，async定义一个协程，await用于挂起阻塞的异步调用接口。

"""
import time
import asyncio
import re
import aiohttp
from aiohttp import ClientSession
import line_profiler

import nest_asyncio #pycharm 不需要
nest_asyncio.apply()#pycharm 不需要

TITLE_PATTERN = re.compile(r'<title.*?>(.*?)</title>', re.DOTALL)

async def fetch_page_title(url):
    async with aiohttp.ClientSession(headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    }) as session:  # type: ClientSession
        async with session.get(url, ssl=False) as resp:
            if resp.status == 200:
                html_code = await resp.text()
                matcher = TITLE_PATTERN.search(html_code)
                title = matcher.group(1).strip()
                print(title)


def main():
    urls = [
        'https://www.python.org/',
        'https://www.jd.com/',
        'https://www.baidu.com/',
        'https://www.taobao.com/',
        'https://git-scm.com/',
        'https://www.sohu.com/',
        'https://gitee.com/',
        'https://www.amazon.com/',
        'https://www.usa.gov/',
        'https://www.nasa.gov/'
    ]
    
    objs = [fetch_page_title(url) for url in urls]
    loop = asyncio.get_event_loop() 
    loop.run_until_complete(asyncio.wait(objs))
 
    #loop.close()


if __name__ == '__main__':

    main()

#---------------------------------------------------------------------------------
import asyncio
import time
#asyncio实现并发，就需要多个协程来完成任务，每当有任务阻塞的时候就await，然后其他协程继续工作
now = lambda: time.time()

async def do_some_work(x):
    print('Waiting: ', x)

    await asyncio.sleep(x)
    return 'Done after {}s'.format(x)

start = now()

coroutine1 = do_some_work(1)
coroutine2 = do_some_work(2)
coroutine3 = do_some_work(4)

tasks = [
    asyncio.ensure_future(coroutine1),
    asyncio.ensure_future(coroutine2),
    asyncio.ensure_future(coroutine3)
]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

for task in tasks:
    print('Task ret: ', task.result())

print('TIME: ', now() - start)
#-----------------------------------------------------------------------------
# 定义异步函数
import time
async def hello():
    await asyncio.sleep(1) #使用await可以针对耗时的操作进行挂起
    print('Hello World:%s' % time.time())

if __name__ =='__main__':
    loop = asyncio.get_event_loop()
    tasks = [hello() for i in range(5)]
    loop.run_until_complete(asyncio.wait(tasks))
    
#-----------------------------------------------------------------------------------    
#协程嵌套
#使用async可以定义协程，协程用于耗时的io操作，我们也可以封装更多的io操作过程，
#这样就实现了嵌套的协程，即一个协程中await了另外一个协程，如此连接起来。
import asyncio

import time

now = lambda: time.time()

async def do_some_work(x):
    print('Waiting: ', x)

    await asyncio.sleep(x)
    return 'Done after {}s'.format(x)

async def main():
    coroutine1 = do_some_work(1)
    coroutine2 = do_some_work(2)
    coroutine3 = do_some_work(4)

    tasks = [
        asyncio.ensure_future(coroutine1),
        asyncio.ensure_future(coroutine2),
        asyncio.ensure_future(coroutine3)
    ]

    dones, pendings = await asyncio.wait(tasks)

    for task in dones:
        print('Task ret: ', task.result())

start = now()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

print('TIME: ', now() - start)
