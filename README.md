# jd_mobile
get jd mobile info

1，获取了京东手机的信息，目前获取数据时，js获取当前用户的地区是写死的，但不影响数据爬取。<br>
2，使用多进程爬取数据，不能将保存数据的初始化连接放到init中。<br>
3，使用gevent协程爬取数据，效率比较高，比多进程高几倍，参考gevent_mobile.py<br>


**遇到的坑**：<br>
>1，多进程中的代码不执行，原因是数据库的连接放到了init中，由于多进程不共享数据造成的。<br>
>2，多进程的Pool进程池不能和gevent同时使用，<br>
>3，多进程中初始化数据库连接不能放在init中，因该是多进程不能共享数据造成多进程程序不运行。<br>


**感想**：
>1，使用多进程时，尽量使自己的程序是单线运行。<br>
>2，使用gevent时，放在最后的for循环最好处理。<br>
>3，gevent 放在循环的地方，循环数据至少5个才能很好看到效果。<br>

**简单示例**<br>
import time<br>
import gevent<br>
from gevent import monkey<br>
monkey.patch_all()<br>
    
    def f1(i):
        time.sleep(5)
        return i

    g_list = []
    for i in range(10):
        g = gevent.spawn(f1,i)
        g_list.append(g)
    items = gevent.joinall(g_list)
    for item in items:
        print('返回值是：',item.value)

