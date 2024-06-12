## eventFilter
>双击触发顺序：MouseButtonPress > MouseButtonRelease > MouseButtonDblClick

## QRunable（没啥卵用）
threadpool是创建线程的对象，它是一个局部变量，会随着线程的消失而瞬间被销毁，所以countBox会在主线程中执行，导致GUI卡死，所以解决办法就是延长该变量的生命周期，因此有以下几种方案：

- 将线程池设为全局变量：
    
    ```csharp
    threadpool = QThreadPool()
    
    def createCounterWorker():
        worker = Worker(countBox)
        threadpool.start(worker)
    ```
    
- 使用QThreadPool.globalInstance()：
    
    ```css
    def createCounterWorker():
        worker = Worker(countBox)
        QThreadPool.globalInstance().start(worker)
    ```