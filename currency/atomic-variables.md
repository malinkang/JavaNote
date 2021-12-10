# 原子类

在编程领域里，原子性意味着“一组操作要么全都操作成功，要么全都失败，不能只操作成功其中的一部分”。而`java.util.concurrent.atomic`下的类，就是具有原子性的类，可以原子性地执行添加、递增、递减等操作。比如之前多线程下的线程不安全的`i++`问题，到了原子类这里，就可以用功能相同且线程安全的`getAndIncrement`方法来优雅地解决。

原子类相比于锁，有一定的优势:

* 粒度更细:原子变量可以把竞争范围缩小到变量级别，通常情况下，锁的粒度都要大于原子变量的粒度。
* 效率更高:除了高度竞争的情况之外，使用原子类的效率通常会比使用同步互斥锁的效率更高，因为原子类底层利用了 CAS 操作，不会阻塞线程。

## 原子类分类

| 类型     | 具体类                                                       |
| -------- | ------------------------------------------------------------ |
| 基本类型 | AtomicInteger、AtomicLong、AtomicBoolean                     |
| 数组类型 | AtomicIntegerArray、AtomicLongArray、AtomicReferenceArray    |
| 引用类型 | AtomicReference、AtomicStampedReference、AtomicMarkableReference |
| 升级类型 | AtomicIntegerfieldupdater、AtomicLongFieldUpdater、AtomicReferenceFieldUpdater |
| 累加器   | LongAdder、DoubleAdder                                       |
| 积累器   | LongAccumulator、DoubleAccumulator                           |


### Adder 

 Adder 和 Accumulator 都是 Java 8 引入的，是相对比较新的类。在高并发下 LongAdder 比 AtomicLong 效率更高，因为对于 AtomicLong 而言，它只适合用 于低并发场景，否则在高并发的场景下，由于 CAS 的冲突概率大，会导致经常自旋，影响整体效率。

 而 LongAdder 引入了分段锁的概念，当竞争不激烈的时候，所有线程都是通过 CAS 对同一个 Base 变量进行修改，但是当竞争 激烈的时候，LongAdder 会把不同线程对应到不同的 Cell 上进行修改，降低了冲突的概率，从而提高了并发性。

### Accumulator 

那么`Accumulator`又是做什么的呢?`Accumulator`和`Adder`非常相似，实际上`Accumulator`就是一个更通用版本的`Adder`，比如`LongAccumulator`是`LongAdder`的功能增强版，因为`LongAdder`的`API`只有对数值的加减，而`LongAccumulator`提供了自定 义的函数操作。

```java
public class LongAccumulatorDemo {
    public static void main(String[] args) throws InterruptedException {
        LongAccumulator accumulator = new LongAccumulator((x,y)->x+y,0);
        ExecutorService executor = Executors.newFixedThreadPool(8);
        IntStream.range(1,10).forEach(i-> executor.submit(()->accumulator.accumulate(i)));
        Thread.sleep(2000);
        System.out.println(accumulator.getThenReset());
    }
}
```
当执行 accumulator.accumulate(1) 的时候，首先要知道这时候 x 和 y 是什么，第一次 执行时， x 是 LongAccumulator 构造函数中的第二个参数，也就是 0，而第一次执行时的 y 值就是本次 accumulator.accumulate(1) 方法所传入的 1;然后根据表达式 x+y，计算出 0+1=1，这个结果会赋值给下一次计算的 x，而下一 次计算的 y 值就是 accumulator.accumulate(2) 传入的 2，所以下一次的计算结果是 1+2=3。

接下来我们说一下 LongAccumulator 的适用场景。 第一点需要满足的条件，就是需要大量的计算，并且当需要并行计算的时候，我们可以考虑使用 LongAccumulator。

当计算量不大，或者串行计算就可以满足需求的时候，可以使用 for 循环;如果计算量大，需要提高计算的效率时，我们则可 以利用线程池，再加上 LongAccumulator 来配合的话，就可以达到并行计算的效果，效率非常高。
第二点需要满足的要求，就是计算的执行顺序并不关键，也就是说它不要求各个计算之间的执行顺序，也就是说线程 1 可能在 线程 5 之后执行，也可能在线程 5 之前执行，但是执行的先后并不影响最终的结果。
一些非常典型的满足这个条件的计算，就是类似于加法或者乘法，因为它们是有交换律的。同样，求最大值和最小值对于顺序 也是没有要求的，因为最终只会得出所有数字中的最大值或者最小值，无论先提交哪个或后提交哪个，都不会影响到最终的结 果。


## 原子类源码分析

以`AtomicInteger`为例，我们来看下`AtomicInteger`是如何通过`CAS`操作实现并发下的累加操作的，以其中一个重要方法`getAndAdd`方法为突破。

```java
private static final jdk.internal.misc.Unsafe U = jdk.internal.misc.Unsafe.getUnsafe();
private static final long VALUE = U.objectFieldOffset(AtomicInteger.class, "value");

public final int getAndAdd(int delta) {
    return U.getAndAddInt(this, VALUE, delta);
}
```

`VALUE`调用 Unsafe 的 objectFieldOffset 方法，从而得到当前这个原子类的 value 的偏移量，并 且赋给 valueOffset 变量，这样一来我们就获取到了 value 的偏移量，它的含义是在内存中的偏移地址，因为 Unsafe 就是根据 内存偏移地址获取数据的原值的，这样我们就能通过 Unsafe 来实现 CAS 了。

`getAndAdd()`调用了 unsafe.getAndAddInt 方法。

### Unsafe 类

Unsafe 类主要是用于和操作系统打交道的，因为大部分的 Java 代码自身无法直接操作内存，所以在必要的时候，可以利用 Unsafe 类来和操作系统进行交互，CAS 正是利用到了 Unsafe 类。

```java
public final int getAndAddInt(Object o, long offset, int delta) {
    int v;
    do {
        v = getIntVolatile(o, offset);
    } while (!weakCompareAndSetInt(o, offset, v, v + delta));
    return v;
}

public final boolean weakCompareAndSetInt(Object o, long offset,
                                          int expected,
                                          int x) {
    return compareAndSetInt(o, offset, expected, x);
}
public native int  getIntVolatile(Object o, long offset);

public final native boolean compareAndSetInt(Object o, long offset,
                                              int expected,
                                              int x);
```

* 第一个参数 object 就是将要操作的对象，传入的是 this，也就是 atomicInteger 这个对象本身;
* 第二个参数是 offset，也就是偏移量，借助它就可以获取到 value 的数值;
* 第三个参数 expectedValue，代表“期望值”，传入的是刚才获取到的 v;
* 而最后一个参数 newValue 是希望修改的数值 ，等于之前取到的数值 v 再加上 delta ，delta 就是我们希望原子类所改变的数值，比如可以传入 +1，也可以传入 -1。

所以 weakCompareAndSetInt 方法的作用就是，判断如果现在原子类里 value 的值和之前获取到的 v 相等的话，那么就把计算出 来的 var5 + var4 给更新上去，所以说这行代码就实现了 CAS 的过程。

一旦 CAS 操作成功，就会退出这个 while 循环，但是也有可能操作失败。如果操作失败就意味着在获取到 v 之后，并且在 CAS 操作之前，value 的数值已经发生变化了，证明有其他线程修改过这个变量。这样一来，就会再次执行循环体里面的代码，重新获取 v 的值，也就是获取最新的原子变量的数值，并且再次利用 CAS 去 尝试更新，直到更新成功为止。

## 原子类和 volatile 的使用场景 

我们可以看出，volatile 和原子类的使用场景是不一样的，如果我们有一个可见性问题，那么可以使用 volatile 关键字，但如果我们的问题是一个组合操作，需要用同步来解决原子性问题的话，那么可以 使用原子变量，而不能使用 volatile 关键字。

通常情况下，volatile 可以用来修饰 boolean 类型的标记位，因为对于标记位来讲，直接的赋值操作本身就是具备原子性的，再加上 volatile 保证了可见性，那么就是线程安全的了。


而对于会被多个线程同时操作的计数器 Counter 的场景，这种场景的一个典型特点就是，它不仅仅是一个简单的赋值操作，而是需要先读取当前的值，然后在此基础上进行一定的修改，再把它给赋值回 去。这样一来，我们的 volatile 就不足以保证这种情况的线程安全了。我们需要使用原子类来保证线程安全。

## 原子类和synchronized区别

1. 原理不同：
    * synchronized:在执行同步代码之前，需要首先获取到 monitor 锁，执行完毕后，再释放锁。
    * 原子类：它保证线程安全的原理是利用了 CAS 操作。

2. 使用范围的不同
    * 原子类的使用范围是比较局限的。因为一个原子类仅仅是一个对象，不够灵活。
    * 而 synchronized 的使用范围要广 泛得多。比如说 synchronized 既可以修饰一个方法，又可以修饰一段代码，相当于可以根据我们的需要，非常灵活地去控制它 的应用范围。

3. 粒度的区别
    * 原子变量的粒度是比较小的，它可以把竞争范围缩小到变量级别。
    * 通常情况下，synchronized 锁的粒度都要大于原子变量的粒度。如果我们只把一行代码用 synchronized 给保护起来的话，有一点杀鸡焉用牛刀的感觉。

4. 性能

因为 synchronized 是一种典型的悲观锁，而原子类恰恰相反，它利用的是乐观锁。所以，我们在比较 synchronized 和 AtomicInteger 的时候，其实也就相当于比较了悲观锁和乐观锁的区别。

从性能上来考虑的话，悲观锁的操作相对来讲是比较重量级的。因为 synchronized 在竞争激烈的情况下，会让拿不到锁的线程 阻塞，而原子类是永远不会让线程阻塞的。不过，虽然 synchronized 会让线程阻塞，但是这并不代表它的性能就比原子类差。

值得注意的是，synchronized 的性能随着 JDK 的升级，也得到了不断的优化。synchronized 会从无锁升级到偏向锁，再升级到 轻量级锁，最后才会升级到让线程阻塞的重量级锁。因此synchronized 在竞争不激烈的情况下，性能也是不错的，不需要“谈虎 色变”。


## 参考

* [Java魔法类：Unsafe应用解析](https://tech.meituan.com/2019/02/14/talk-about-java-magic-class-unsafe.html)