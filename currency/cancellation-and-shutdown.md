# 取消与关闭

任务和线程的启动很容易，在大多数时候，我们都会让它们运行直到结束，或者让它们自行停止。然后，有时候我们希望提前结束任务或线程，或许是因为用户取消了操作，或者应用程序需要被快速关闭。

要使任务和线程能安全、快速、可靠地停止下来，并不是一件容易的事。Java没有提供任何机制来安全地终止线程。但它提供了中断（Interruption），这是一种协作机制，能够使一个线程终止另一个线程的当前工作。

<!--more-->

## 7.1 任务取消

## 7.2 停止基于线程的服务


### 7.2.2 关闭ExecutorService

`ExecutorService`提供了两种关闭方法：使用`shutdown`正常关闭，以及使用`shutdownNow`强行关闭。在进行强行关闭时，`shutdownNow`首先关闭当前正在执行的任务，然后返回所有尚未启动的任务清单。

这两种关闭方式的差别在于各自的安全性和响应性：强制关闭的速度更快，但风险也更大，因为任务很可能在执行到一半时被结束：而正常关闭虽然速度慢，但却更安全，因为`ExecutorService`会一直等到队列中的所有任务都执行完成后才关闭。在其他拥有线程的服务中也应该考虑提供类似的关闭方式以供选择。



## 7.4 JVM关闭