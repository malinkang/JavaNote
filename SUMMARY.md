# Table of contents

* [Introduction](README.md)
* [面试题整理](interview.md)

## 《Java编程思想》

* [第2章一切都是对象](thinking-in-java/everything-is-an-object.md)
* [第3章操作符](thinking-in-java/operators.md)
* [第4章控制流程](thinking-in-java/controlling-execution.md)
* [第5章初始化与清理](thinking-in-java/initialization-and-cleanup.md)
* [第6章访问权限控制](thinking-in-java/access-control.md)
* [第7章复用类](thinking-in-java/reusing-classes.md)
* [第8章多态](thinking-in-java/polymorphism.md)
* [第9章接口](thinking-in-java/interfaces.md)
* [第10章内部类](thinking-in-java/inner-classes.md)
* [第11章持有对象](thinking-in-java/holding-your-objects.md)
* [第12章通过异常处理错误](thinking-in-java/error-handling-with-exceptions.md)
* [第13章字符串](thinking-in-java/strings.md)
* [第14章类型信息](thinking-in-java/type-information.md)
* [第15章泛型](thinking-in-java/generics.md)
* [第16章数组](thinking-in-java/arrays.md)
* [第17章容器深入研究](thinking-in-java/containers-in-depth.md)
* [第18章I/O系统](thinking-in-java/i-o.md)
* [第19章枚举类型](thinking-in-java/enumerated-types.md)
* [第20章注解](thinking-in-java/annotations.md)
* [第21章并发](thinking-in-java/concurrency.md)

## 《Effective Java》

* [第2章创建和销毁对象](effective-java/creating-and-destroying-objects.md)
* [第3章对于所有对象都通用的方法](effective-java/methods-common-to-all-objects.md)
* [第4章类和接口](effective-java/classes-and-interfaces.md)
* [第5章泛型](effective-java/generics.md)
* [第6章枚举和注解](effective-java/enums-and-annotations.md)
* [第7章lambda表达式和流](effective-java/lambdas-and-streams.md)
* [第8章方法](effective-java/methods.md)
* [第9章通用程序设计](effective-java/general-programming.md)
* [第10章异常](effective-java/exceptions.md)
* [第11章并发](effective-java/concurrency.md)
* [第12章序列化](effective-java/serialization.md)

## jvm 

* [Java内存区域与内存溢出](jvm/runtime-data-areas.md)
* [垃圾收集器与内存分配策略](jvm/garbage-collection.md)
* [类文件结构](jvm/class-file-structure.md)
* [虚拟机类加载机制](jvm/classloader.md)
* [虚拟机字节码执行引擎](jvm/execution-engin.md)
* [编译期优化](jvm/compilation-optimization.md)
* [Java内存模型与线程](jvm/java-memory-model-and-thread.md)
* [线程安全与锁优化](jvm/thread-safe-and-lock-optimization.md)

## 并发

* [原子变量与非阻塞同步机制](currency/atomic-variables-and-nonblocking-synchronization.md)
* [基础构建模块](currency/building-blocks.md)
* [构建自定义的同步工具](currency/building-custom-synchronizers.md)
* [取消与关闭](currency/cancellation-and-shutdown.md)
* [显式锁](currency/explicit-locks.md)
* [对象的共享](currency/sharing-objects.md)
* [任务执行](currency/task-execution.md)
* [Java内存模型](currency/the-java-momory-model.md)
* [线程池](currency/thread-pools.md)
* [线程安全](currency/synchronized.md)
* [CAS](currency/compare-and-swap.md)
* [原子变量](currency/atomic-variables.md)
* [final](currency/final.md)
* [threadlocal](currency/threadlocal.md)
* [aqs](currency/aqs.md)
* [callable](currency/callable.md)
* [future](currency/future.md)

## 并发编程78讲

* 究竟什么是线程安全？
 * [第08讲-为什么多线程会带来性能问题](78/究竟什么是线程安全？/第08讲-为什么多线程会带来性能问题-.md)
 * [第06讲-一共有哪 3 类线程安全问题](78/究竟什么是线程安全？/第06讲-一共有哪 3 类线程安全问题-.md)
* 死锁问题
 * [第68讲-发生死锁必须满足哪 4 个条件](78/死锁问题/第68讲-发生死锁必须满足哪 4 个条件-.md)
 * [第70讲-有哪些解决死锁问题的策略](78/死锁问题/第70讲-有哪些解决死锁问题的策略-.md)
 * [第69讲-如何用命令行和代码定位死锁](78/死锁问题/第69讲-如何用命令行和代码定位死锁-.md)
 * [第71讲-讲一讲经典的哲学家就餐问题.md](78/死锁问题/第71讲-讲一讲经典的哲学家就餐问题.md)
 * [第67讲-如何写一个必然死锁的例子](78/死锁问题/第67讲-如何写一个必然死锁的例子-.md)
* 开篇
 * [开篇词- 由点及面，搭建你的 Java 并发知识网.md](78/开篇/开篇词- 由点及面，搭建你的 Java 并发知识网.md)
* 线程基础升华
 * [第05讲-有哪几种实现生产者消费者模式的方法](78/线程基础升华/第05讲-有哪几种实现生产者消费者模式的方法-.md)
 * [第04讲-wait-notify-notifyAll 方法的使用注意事项](78/线程基础升华/第04讲-wait-notify-notifyAll 方法的使用注意事项-.md)
 * [第03讲-线程是如何在 6 种状态之间转换的](78/线程基础升华/第03讲-线程是如何在 6 种状态之间转换的-.md)
 * [第02讲-如何正确停止线程-为什么 volatile 标记位的停止方法是错误的](78/线程基础升华/第02讲-如何正确停止线程-为什么 volatile 标记位的停止方法是错误的-.md)
 * [第01讲-为何说只有 1 种实现线程的方法](78/线程基础升华/第01讲-为何说只有 1 种实现线程的方法-.md)
* Java 内存模型
 * [第63讲-单例模式的双重检查锁模式为什么必须加 volatile](78/Java 内存模型/第63讲-单例模式的双重检查锁模式为什么必须加 volatile-.md)
 * [第59讲-什么是“内存可见性”问题](78/Java 内存模型/第59讲-什么是“内存可见性”问题-.md)
 * [第60讲-主内存和工作内存的关系](78/Java 内存模型/第60讲-主内存和工作内存的关系-.md)
 * [第57讲-什么是指令重排序-为什么要重排序](78/Java 内存模型/第57讲-什么是指令重排序-为什么要重排序-.md)
 * [第56讲-讲一讲什么是 Java 内存模型](78/Java 内存模型/第56讲-讲一讲什么是 Java 内存模型-.md)
 * [第61讲-什么是 happens-before 规则](78/Java 内存模型/第61讲-什么是 happens-before 规则-.md)
 * [第58讲-Java 中的原子操作有哪些注意事项](78/Java 内存模型/第58讲-Java 中的原子操作有哪些注意事项-.md)
 * [第62讲-volatile 的作用是什么-与 synchronized 有什么异同](78/Java 内存模型/第62讲-volatile 的作用是什么-与 synchronized 有什么异同-.md)
* 各种各样的“锁”
 * [第21讲-如何看到 synchronized 背后的“monitor 锁”](78/各种各样的“锁”/第21讲-如何看到 synchronized 背后的“monitor 锁”-.md)
 * [第19讲-你知道哪几种锁-分别有什么特点](78/各种各样的“锁”/第19讲-你知道哪几种锁-分别有什么特点-.md)
 * [第28讲-JVM 对锁进行了哪些优化](78/各种各样的“锁”/第28讲-JVM 对锁进行了哪些优化-.md)
 * [第26讲-读锁应该插队吗-什么是读写锁的升降级](78/各种各样的“锁”/第26讲-读锁应该插队吗-什么是读写锁的升降级-.md)
 * [第25讲-读写锁 ReadWriteLock 获取锁有哪些规则](78/各种各样的“锁”/第25讲-读写锁 ReadWriteLock 获取锁有哪些规则-.md)
 * [第27讲-什么是自旋锁-自旋的好处和后果是什么呢](78/各种各样的“锁”/第27讲-什么是自旋锁-自旋的好处和后果是什么呢-.md)
 * [第22讲-synchronized 和 Lock 孰优孰劣，如何选择](78/各种各样的“锁”/第22讲-synchronized 和 Lock 孰优孰劣，如何选择-.md)
 * [第24讲-讲一讲公平锁和非公平锁，为什么要“非公平”](78/各种各样的“锁”/第24讲-讲一讲公平锁和非公平锁，为什么要“非公平”-.md)
 * [第23讲-Lock 有哪几个常用方法-分别有什么用](78/各种各样的“锁”/第23讲-Lock 有哪几个常用方法-分别有什么用-.md)
* 线程协作
 * [第54讲-CyclicBarrier 和 CountdownLatch 有什么异同](78/线程协作/第54讲-CyclicBarrier 和 CountdownLatch 有什么异同-.md)
 * [第52讲-信号量能被 FixedThreadPool 替代吗](78/线程协作/第52讲-信号量能被 FixedThreadPool 替代吗-.md)
 * [第53讲-CountDownLatch 是如何安排线程执行顺序的](78/线程协作/第53讲-CountDownLatch 是如何安排线程执行顺序的-.md)
 * [第55讲-Condition、object.wait() 和 notify() 的关系](78/线程协作/第55讲-Condition、object.wait() 和 notify() 的关系-.md)
* 总结
 * [第78讲-一份独家的 Java 并发工具图谱.md](78/总结/第78讲-一份独家的 Java 并发工具图谱.md)
 * [参考文献、版权声明、致谢.md](78/总结/参考文献、版权声明、致谢.md)
* AQS 框架
 * [第75讲-为什么需要 AQS-AQS 的作用和重要性是什么](78/AQS 框架/第75讲-为什么需要 AQS-AQS 的作用和重要性是什么-.md)
 * [第77讲-AQS 在 CountDownLatch 等类中的应用原理是什么](78/AQS 框架/第77讲-AQS 在 CountDownLatch 等类中的应用原理是什么-.md)
 * [第76讲-AQS 的内部原理是什么样的](78/AQS 框架/第76讲-AQS 的内部原理是什么样的-.md)
* Future 掌控未来
 * [第49讲-Future 的主要功能是什么](78/Future 掌控未来/第49讲-Future 的主要功能是什么-.md)
 * [第51讲-如何利用 CompletableFuture 实现“旅游平台”问题](78/Future 掌控未来/第51讲-如何利用 CompletableFuture 实现“旅游平台”问题-.md)
 * [第48讲-Callable 和 Runnable 的不同](78/Future 掌控未来/第48讲-Callable 和 Runnable 的不同-.md)
 * [第50讲-使用 Future 有哪些注意点-Future 产生新的线程了吗](78/Future 掌控未来/第50讲-使用 Future 有哪些注意点-Future 产生新的线程了吗-.md)
 * [第48讲-Callable 和 Runnable 的不同-的副本.md](78/Future 掌控未来/第48讲-Callable 和 Runnable 的不同-的副本.md)
* ThreadLocal
 * [第46讲-多个 ThreadLocal 在 Thread 中的 threadlocals 里是怎么存储的](78/ThreadLocal/第46讲-多个 ThreadLocal 在 Thread 中的 threadlocals 里是怎么存储的-.md)
 * [第47讲-内存泄漏——为何每次用完 ThreadLocal 都要调用 remove()](78/ThreadLocal/第47讲-内存泄漏——为何每次用完 ThreadLocal 都要调用 remove()-.md)
 * [第44讲-ThreadLocal 适合用在哪些实际生产的场景中](78/ThreadLocal/第44讲-ThreadLocal 适合用在哪些实际生产的场景中-.md)
 * [第45讲-ThreadLocal 是用来解决共享资源的多线程访问的问题吗](78/ThreadLocal/第45讲-ThreadLocal 是用来解决共享资源的多线程访问的问题吗-.md)
* CAS 原理
 * [第64讲-你知道什么是 CAS 吗](78/CAS 原理/第64讲-你知道什么是 CAS 吗-.md)
 * [第65讲-CAS 和乐观锁的关系，什么时候会用到 CAS](78/CAS 原理/第65讲-CAS 和乐观锁的关系，什么时候会用到 CAS-.md)
 * [第66讲-CAS 有什么缺点](78/CAS 原理/第66讲-CAS 有什么缺点-.md)
* test.py
* 线程池
 * [第09讲-使用线程池比手动创建线程好在哪里](78/线程池/第09讲-使用线程池比手动创建线程好在哪里-.md)
 * [第10讲-线程池的各个参数的含义](78/线程池/第10讲-线程池的各个参数的含义-.md)
 * [第12讲-有哪 6 种常见的线程池-什么是 Java8 的 ForkJoinPool](78/线程池/第12讲-有哪 6 种常见的线程池-什么是 Java8 的 ForkJoinPool-.md)
 * [第18讲-线程池实现“线程复用”的原理](78/线程池/第18讲-线程池实现“线程复用”的原理-.md)
 * [第11讲-线程池有哪 4 种拒绝策略](78/线程池/第11讲-线程池有哪 4 种拒绝策略-.md)
 * [第15讲-合适的线程数量是多少-CPU 核心数和线程数的关系](78/线程池/第15讲-合适的线程数量是多少-CPU 核心数和线程数的关系-.md)
 * [第17讲-如何正确关闭线程池-shutdown 和 shutdownNow 的区别](78/线程池/第17讲-如何正确关闭线程池-shutdown 和 shutdownNow 的区别-.md)
 * [第16讲-如何根据实际需要，定制自己的线程池](78/线程池/第16讲-如何根据实际需要，定制自己的线程池-.md)
 * [第14讲-为什么不应该自动创建线程池](78/线程池/第14讲-为什么不应该自动创建线程池-.md)
 * [第13讲-线程池常用的阻塞队列有哪些](78/线程池/第13讲-线程池常用的阻塞队列有哪些-.md)
* 并发容器面面观
 * [第33讲-CopyOnWriteArrayList 有什么特点](78/并发容器面面观/第33讲-CopyOnWriteArrayList 有什么特点-.md)
 * [第29讲-HashMap 为什么是线程不安全的](78/并发容器面面观/第29讲-HashMap 为什么是线程不安全的-.md)
 * [第32讲-同样是线程安全，ConcurrentHashMap 和 Hashtable 的区别](78/并发容器面面观/第32讲-同样是线程安全，ConcurrentHashMap 和 Hashtable 的区别-.md)
 * [第31讲-为什么 Map 桶中超过 8 个才转为红黑树](78/并发容器面面观/第31讲-为什么 Map 桶中超过 8 个才转为红黑树-.md)
 * [第30讲-ConcurrentHashMap 在 Java7 和 8 有何不同](78/并发容器面面观/第30讲-ConcurrentHashMap 在 Java7 和 8 有何不同-.md)
* 原子类
 * [第42讲-AtomicInteger 和 synchronized 的异同点](78/原子类/第42讲-AtomicInteger 和 synchronized 的异同点-.md)
 * [第41讲-原子类和 volatile 有什么异同](78/原子类/第41讲-原子类和 volatile 有什么异同-.md)
 * [第39讲-原子类是如何利用 CAS 保证线程安全的](78/原子类/第39讲-原子类是如何利用 CAS 保证线程安全的-.md)
 * [第43讲-Java 8 中 Adder 和 Accumulator 有什么区别](78/原子类/第43讲-Java 8 中 Adder 和 Accumulator 有什么区别-.md)
 * [第40讲-AtomicInteger 在高并发下性能不好，如何解决-为什么](78/原子类/第40讲-AtomicInteger 在高并发下性能不好，如何解决-为什么-.md)
* 阻塞队列
 * [第37讲-阻塞和非阻塞队列的并发安全原理是什么](78/阻塞队列/第37讲-阻塞和非阻塞队列的并发安全原理是什么-.md)
 * [第34讲-什么是阻塞队列](78/阻塞队列/第34讲-什么是阻塞队列-.md)
 * [第36讲-有哪几种常见的阻塞队列](78/阻塞队列/第36讲-有哪几种常见的阻塞队列-.md)
 * [第38讲-如何选择适合自己的阻塞队列](78/阻塞队列/第38讲-如何选择适合自己的阻塞队列-.md)
 * [第35讲-阻塞队列包含哪些常用的方法-add、offer、put 等方法的区别](78/阻塞队列/第35讲-阻塞队列包含哪些常用的方法-add、offer、put 等方法的区别-.md)
* final 关键字和“不变性”
 * [第72讲-final 的三种用法是什么](78/final 关键字和“不变性”/第72讲-final 的三种用法是什么-.md)
 * [第73讲-为什么加了 final 却依然无法拥有“不变性”](78/final 关键字和“不变性”/第73讲-为什么加了 final 却依然无法拥有“不变性”-.md)
 * [第74讲-为什么 String 被设计为是不可变的](78/final 关键字和“不变性”/第74讲-为什么 String 被设计为是不可变的-.md)
