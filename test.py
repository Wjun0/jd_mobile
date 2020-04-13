#coding:utf8
from multiprocessing import Pool
import time


class T(object):

    def p(self,i):
        time.sleep(2)
        return i


    def t1(self,i):
        print("t1",i)
        time.sleep(2)
        da = self.p(i)
        print("p的结果：",da)
        return i


    def run(self,):
        print("start ")
        p = Pool()
        for i in range(20):
            p.apply_async(self.t1, args=(i,))
        p.close()
        p.join()
        print("end")


if __name__ == '__main__':
    start_time = time.time()
    t = T()
    t.run()
    print("耗时：",start_time-time.time())

