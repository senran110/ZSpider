## 1、协程锁的作用
**由来：**
一开始自认为协程是单线程间切换就不需要锁了抱着问题搜索了一番。

**解答：**
协程虽然是单线程调度，但由于执行中有延时或者I/O中断等因素，如下代码四个协程不加锁输出a的值分别为4，3，2，1不符合预期。
```
import asyncio
import time

a = 1
lock = asyncio.Lock()

# 模拟IO任务
async def test(i):
    await asyncio.sleep(i)
    print(i)


async def run(i):
	# 锁
    # async with lock:
    global a
    print("第{}个协程start".format(i))
    a += 1
	# await 时会显式切换
    await asyncio.sleep(1)
    a -= 1
    print("第{}个协程:{}".format(i, a))


if __name__ == '__main__':
    print(f"started at {time.strftime('%X')}")
    tasks = [asyncio.ensure_future(run(i)) for i in range(1, 5)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    print(f"finished at {time.strftime('%X')}")
```

## 2、多线程什么时候需要加锁？
一般可能“同时发生多个写操作”或“同时发生读写操作”时，必需要加Lock，多人读则不必加锁。

## 3、Pycharm
Pycharm的Structure图标上的字母是简写，自动补全为变量的类别  
p：parameter 参数  
m：method 方法  
c：class 类  
v：variable 变量  
f：function 函数  
