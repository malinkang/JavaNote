# 对象的共享

我们已经知道了同步代码块和同步方法可以确保以原子的方式执行操作，但一种常见的误解是，认为关键字`synchronized`只能用于实现原子性或者确定临界区。同步还有另一个重要的方面：内存可见性（Memory Visibility）。我们不仅希望防止某个线程正在使用对象状态而另一个线程在同时修改该状态，而且希望确保当一个线程修改了对象状态后，其他线程能够看到发生的状态变化。如果没有同步，那么这种情况就无法实现。你可以通过显式的同步或者类库中内置的同步来保证对象被安全地发布。

<!--more-->

## 3.1 可见性

### 3.1.1 失效数据

### 3.1.2 非原子的64位操作

### 3.1.3 加锁与可见性

### 3.1.4 Volatile变量

`Java`语言提供了一种稍弱的同步机制，即volatile变量，用来确保将变量的更新操作通知到其他线程。当把变量声明为`volatile`类型后，编译器与运行时都会注意到这个变量是共享的，因此不会将该变量上的操作与其他内存操作一起重排序。volatile变量不会被缓存在寄存器或者对其他处理器不可见的地方，因此在读取`volatile`类型的变量时总会返回最新写入的值。

在访问`volatile`变量时不会执行加锁操作，也就不会执行线程阻塞，因此volatile变量是一种比`synchronized`关键字更轻量级的同步机制。

当且仅当满足以下所有条件时，才应该使用volatile变量：

* 对变量的写入操作不依赖变量的当前值，或者你能确保只有单个线程更新变量的值。
* 该变量不会与其他状态变量一起纳入不变性条件中。
* 在访问变量时不需要加锁。


## 3.2 发布与逸出

## 3.3 线程封闭

### 3.3.1 Ad-hoc线程封闭

### 3.3.2 栈封闭

### 3.3.3 ThreadLocal类

## 3.4 不变性

满足同步需求的另一种方法是使用不可变对象（Immutable Object）。到目前为止，我们介绍了许多与原子性和可见性相关的问题，例如得到失效数据，丢失更新操作或者观察到某个对象处于不一致的状态等等，都与多线程试图同时访问同一个可变的状态相关。如果对象的状态不会改变，那么这些问题与复杂性也就自然消失了。

如果某个对象在被创建后其状态就不能被修改，那么这个对象就称为不可变对象。线程安全性是不可变对象的固有属性之一，它们的不可变性条件是由构造函数创建的，只要它们的状态不改变，那么这些不变性条件就能得到维持。

### 3.4.1 Final域

## 3.5 安全发布



## 参考

* [第62讲：volatile 的作用是什么？与 synchronized 有什么异同？](https://kaiwu.lagou.com/course/courseInfo.htm?courseId=16#/detail/pc?id=300)

