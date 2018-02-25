

import multiprocessing
from multiprocessing import Process, Queue

import time
import random

import sys

import mod_wsgi

print(mod_wsgi.__path__)

print(sys.executable)


def worker(num, cmd, q):
    """worker function"""
    time.sleep(random.randint(5, 20))
    print('Worker', num, cmd)

    q.put(num)

    return


# def consumer(q):
#
#     while True:
#
#         data = q.get()
#
#         if data == 0:
#             break


#
# if __name__ == '__main__':
#     jobs = []
#
#     queue = Queue()
#
#     for i in range(5):
#         p = multiprocessing.Process(target=worker, args=(i, 'cmd', queue))
#         jobs.append(p)
#         p.start()
#
#     time.sleep(1)
#
#     while True:
#
#         while True:
#
#             if queue.empty():
#                 break
#
#             obj = queue.get()
#             print('obj=', obj)
#
#
#
#
#     # print(jobs)
#
#
#
