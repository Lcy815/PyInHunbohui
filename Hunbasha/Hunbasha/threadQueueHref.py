# encoding=utf-8
import threading
import queue
import time


class Worker(threading.Thread):
    def __init__(self, one_q):
        threading.Thread.__init__(self)
        self.queue = one_q
        self.thread_stop = False

    def run(self):
        while not self.thread_stop:
            try:
                task = self.queue.get(block=True, timeout=20)
            except queue.Empty:
                print("nothing to do")
                self.thread_stop = True
                break
            print(task[0], task[1])
            time.sleep(3)
            self.queue.task_done()

    def stop(self):
        self.thread_stop = True

if __name__ == '__main__':
    q = queue.Queue(5)
    work = Worker(q)
    work.start()
    q.put(["produce one cup!", 1], block=True, timeout=None)  # 产生任务消息
    q.put(["produce one desk!", 2], block=True, timeout=None)
    q.put(["produce one apple!", 3], block=True, timeout=None)
    q.put(["produce one banana!", 4], block=True, timeout=None)
    q.put(["produce one bag!", 5], block=True, timeout=None)
    print("***************leader:wait for finish!")
    q.join()  # 等待所有任务完成
    print("***************leader:all task finished!")




