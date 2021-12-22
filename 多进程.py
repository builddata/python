# -*- coding: utf-8 -*-
"""
多进程
程序执行计算密集型任务（如：音视频编解码、数据压缩、科学计算等）
程序的输入可以并行的分成块，并且可以将运算结果合并
程序在内存使用方面没有任何限制且不强依赖于 I/O 操作（如读写文件、套接字等）
对于爬虫这类 I/O 密集型任务来说，使用多进程并没有什么优势；但是对于计算密集型任务来说，
多进程相比多线程，在效率上会有显著的提升

在 Python 中可以基于Process类来创建进程，虽然进程和线程有着本质的差别，
但是Process类和Thread类的用法却非常类似。在使用Process类的构造器创建对象时，
也是通过target参数传入一个函数来指定进程要执行的代码
"""

from multiprocessing import Process, current_process,Queue
from time import sleep
import time
#由于多个进程之间不能够像多个线程之间直接通过共享内存的方式交换数据，
#要解决这个问题比较简单的办法是使用multiprocessing模块中的Queue类，
#它是可以被多个进程共享的队列，底层是通过操作系统底层的管道和信号量（semaphore）机制来实现的
def sub_task(content, queue):
    counter = queue.get()
    while counter < 50:
        print(content, end='', flush=True)
        counter += 1
        queue.put(counter)
        time.sleep(0.01)
        counter = queue.get()


def main():
    queue = Queue()
    queue.put(0)
    p1 = Process(target=sub_task, args=('Ping', queue))
    p1.start()
    p2 = Process(target=sub_task, args=('Pong', queue))
    p2.start()
    while p1.is_alive() and p2.is_alive():
        pass
    queue.put(50)


if __name__ == '__main__':
    main()
#-------------------------------------------------------------------------------  

import concurrent.futures
PRIMES = [1116281,1297337,104395303,472882027,533000389,817504243] * 5
def is_prime(n):
    """判断素数"""
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return n != 1

def main():
    """主函数"""
    with concurrent.futures.ProcessPoolExecutor(max_workers=16) as executor:
        for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
            print('%d is prime: %s' % (number, prime)) 
            
if __name__ == '__main__':
    main()  
    
#-------------------------------------------------------------------------------     
    
    
    
    
    