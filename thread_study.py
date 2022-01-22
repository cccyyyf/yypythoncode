# @Time: 2021/12/13 22:57
# @Auth: Margot

import logging
import _thread
import threading
from time import ctime, sleep

logging.basicConfig(level=logging.INFO)
loops=[2,6]

# def loop(n, sec, lock):
#     logging.info("start loop" + str(n) + "at" + ctime())
#     sleep(sec)
#     logging.info("end loop" + str(n) + "at" + ctime())
#     lock.release()
#
# def main():
#     logging.info("start all loop at" + ctime())
#     locks = []
#     n = range(len(loops))
#     for i in n:
#         lock = _thread.allocate_lock()    #返回一个新的锁对象
#         lock.acquire()
#         locks.append(lock)
#     for i in n:
#         _thread.start_new_thread(loop, (i, loops[i], locks[i]))
#     for i in n:
#         while locks[i].locked(): pass
#     logging.info("end all loop at" + ctime())


#使用threading
def loop(n, sec):
    logging.info("start loop" + str(n) + "at" + ctime())
    sleep(sec)
    logging.info("end loop" + str(n) + "at" + ctime())

def main():
    logging.info("start all loop at" + ctime())
    threads = []
    n = range(len(loops))
    for i in n:
        t = threading.Thread(target=loop, args=(i, loops[i]))
        threads.append(t)
    for i in n:
        threads[i].start()
    for i in n:
        threads[i].join()
    logging.info("end all loop at" + ctime())


if __name__ == '__main__':
    main()
