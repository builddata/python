# -*- coding: utf-8 -*-
"""
多线程：使用threading模块
线程是操作系统分配CPU的基本单位，进程是操作系统分配内存的基本单位。
通常我们运行的程序会包含一个或多个进程，而每个进程中又包含一个或多个线程。
多线程的优点在于多个线程可以共享进程的内存空间，所以进程间的通信非常容易实现；
多线程适合那些会花费大量时间在I/O操作上，但没有太多并行计算需求且不需占用太多内存的I/O密集型应用。
"""
#我们可以直接使用threading模块的Thread类来创建线程，但是我们之前讲过一个非常重要的概念叫“继承”，
#我们可以从已有的类创建新类，因此也可以通过继承Thread类的方式来创建自定义的线程类，
#然后再创建线程对象并启动线程。
from random import randint
from threading import Thread
from time import time, sleep

class DownloadTask(Thread):

    def __init__(self, filename):
        super().__init__()
        self._filename = filename

    def run(self):
        print('开始下载%s...' % self._filename)
        time_to_download = randint(5, 10)
        sleep(time_to_download)
        print('%s下载完成! 耗费了%d秒' % (self._filename, time_to_download))

def main():
    start = time()
    t1 = DownloadTask('Python从入门到住院.pdf')
    t1.start()
    t2 = DownloadTask('Peking Hot.avi')
    t2.start()
    t1.join()
    t2.join()
    end = time()
    print('总共耗费了%.2f秒.' % (end - start))

if __name__ == '__main__':
    main()
#----------------------------------------------------------------------------------------
#利用线程池，可以提前准备好若干个线程，在使用的过程中不需要再通过自定义的代码创建和释放线程，
#而是直接复用线程池中的线程。Python 内置的concurrent.futures模块提供了对线程池的支持
import random
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
def download(*, filename):
    start = time.time()
    print(f'开始下载 {filename}.')
    time.sleep(random.randint(3, 6))
    print(f'{filename} 下载完成.')
    end = time.time()
    print(f'下载耗时: {end - start:.3f}秒.')

def main():
    with ThreadPoolExecutor(max_workers=4) as pool:
        filenames = ['Python从入门到住院.pdf', 'MySQL从删库到跑路.avi', 'Linux从精通到放弃.mp4']
        start = time.time()
        for filename in filenames:
            pool.submit(download, filename=filename)
        end = time.time()
    print(f'总耗时: {end - start:.3f}秒.')

if __name__ == '__main__':
    main()

#----------------------------------------------------------------------------------------
from threading import RLock

class Account(object):
    """银行账户"""

    def __init__(self):
        self.balance = 0.0
        self.lock = RLock()  #加锁让函数变为线程安全的函数

    def deposit(self, money):
        # 通过上下文语法获得锁和释放锁
        with self.lock:
            new_balance = self.balance + money
            time.sleep(0.01)
            self.balance = new_balance

def main():
    """主函数"""
    account = Account()
    with ThreadPoolExecutor(max_workers=16) as pool:
        for _ in range(100):
            pool.submit(account.deposit, 1)
    print(account.balance)

if __name__ == '__main__':
	main()

#----------------------------------------------------------------------------------------

















