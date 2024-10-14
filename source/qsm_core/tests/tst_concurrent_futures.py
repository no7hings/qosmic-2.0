# coding:utf-8
from concurrent.futures import ThreadPoolExecutor

# 创建一个全局线程池
executor = ThreadPoolExecutor(max_workers=5)

# 限制递归深度
MAX_RECURSION_DEPTH = 3


def fibonacci(n, depth=0):
    print n, depth
    if n <= 1:
        return

    # 提交两个子任务
    future1 = executor.submit(fibonacci, n-1, depth+1)
    future2 = executor.submit(fibonacci, n-2, depth+1)

    # a = future1.result()
    # b = future2.result()
    # # 等待结果
    # return a+b


# 计算第 5 个斐波那契数
result = fibonacci(5)
print 'The 5th Fibonacci number is:', result

# 关闭线程池
executor.shutdown(wait=True)



