# 原子变量与非阻塞同步机制

在`java.util.concurrent`包的许多类中，例如`Semaphore`和`ConcurrentLinkedQueue`，都提供了比`synchronized`机制更高的性能和可伸缩性。

<!--more-->

## 锁的劣势

## 硬件对并发的支持

### 比较并交换

### 非阻塞的计数器

### JVM对CAS的支持

## 原子变量类



共有12个原子变量类，可分为4组：

* 标量类（Scalar）、
* 更新器类、
* 数组类以
* 复合变量类。

最常用的原子变量就是标量类：`AtomicInteger`、`AtomicLong`、`AtomicBoolean`以及`AtomicReference`。所有这些类都支持CAS，此外，`AtomicInteger`和`AtomicLong`还支持算数运算符。（要想模拟其他基本类型的原子变量，可以将short或byte等类型与int类型进行转换，以及使用floatToBits或doubleToLongBits来转换浮点数。）

### 15.3.1 原子变量是一种“更好的volatile”

### 性能比较：锁与原子变量

原子类相比于锁，有一定的优势:

* 粒度更细:原子变量可以把竞争范围缩小到变量级别，通常情况下，锁的粒度都要大于原子变量的粒度。
* 效率更高:除了高度竞争的情况之外，使用原子类的效率通常会比使用同步互斥锁的效率更高，因为原子类底层利用了 CAS 操作，不会阻塞线程。

## 15.4 非阻塞算法

### 15.4.1 非阻塞的栈

### 15.4.2 非阻塞的链表

### 15.4.3 原子的域更新器

### 15.4.4 ABA问题

