
在 Java&nbsp;8 中，对于 ConcurrentHashMap 这个常用的工具类进行了很大的升级，对比之前 Java&nbsp;7 版本在诸多方面都进行了调整和变化。不过，在 Java&nbsp;7 中的 Segment 的设计思想依然具有参考和学习的价值，所以在很多情况下面试官都会问你：ConcurrentHashMap 在 Java 7 和 Java&nbsp;8 中的结构分别是什么？它们有什么相同点和不同点？所以本课时就对 ConcurrentHashMap 在这两个版本的特点和性质进行对比和介绍。

### Java 7 版本的 ConcurrentHashMap

我们首先来看一下 Java&nbsp;7 版本中的 ConcurrentHashMap 的结构示意图：

<img src="https://s0.lgstatic.com/i/image3/M01/61/20/CgpOIF4b3hKAfFsTAAG5MQvpc-w836.png" alt="">

从图中我们可以看出，在 ConcurrentHashMap 内部进行了 Segment 分段，Segment 继承了 ReentrantLock，可以理解为一把锁，各个 Segment 之间都是相互独立上锁的，互不影响。相比于之前的 Hashtable 每次操作都需要把整个对象锁住而言，大大提高了并发效率。因为它的锁与锁之间是独立的，而不是整个对象只有一把锁。

每个 Segment 的底层数据结构与 HashMap 类似，仍然是数组和链表组成的拉链法结构。默认有 0~15 共 16 个 Segment，所以最多可以同时支持 16 个线程并发操作（操作分别分布在不同的 Segment 上）。16 这个默认值可以在初始化的时候设置为其他值，但是一旦确认初始化以后，是不可以扩容的。

### Java 8 版本的 ConcurrentHashMap

在 Java 8 中，几乎完全重写了 ConcurrentHashMap，代码量从原来 Java 7 中的 1000 多行，变成了现在的 6000 多行，所以也大大提高了源码的阅读难度。而为了方便我们理解，我们还是先从整体的结构示意图出发，看一看总体的设计思路，然后再去深入细节。

<img src="https://s0.lgstatic.com/i/image3/M01/61/21/Cgq2xl4b3oCAAFxPAAGZw5NzqtE099.png" alt="">

图中的节点有三种类型。

- 第一种是最简单的，空着的位置代表当前还没有元素来填充。
- 第二种就是和 HashMap 非常类似的拉链法结构，在每一个槽中会首先填入第一个节点，但是后续如果计算出相同的 Hash 值，就用链表的形式往后进行延伸。
- 第三种结构就是红黑树结构，这是 Java 7 的 ConcurrentHashMap 中所没有的结构，在此之前我们可能也很少接触这样的数据结构。

当第二种情况的链表长度大于某一个阈值（默认为 8），且同时满足一定的容量要求的时候，ConcurrentHashMap 便会把这个链表从链表的形式转化为红黑树的形式，目的是进一步提高它的查找性能。所以，Java 8 的一个重要变化就是引入了红黑树的设计，由于红黑树并不是一种常见的数据结构，所以我们在此简要介绍一下红黑树的特点。

红黑树是每个节点都带有颜色属性的二叉查找树，颜色为红色或黑色，红黑树的本质是对二叉查找树 BST 的一种平衡策略，我们可以理解为是一种平衡二叉查找树，查找效率高，会自动平衡，防止极端不平衡从而影响查找效率的情况发生。

由于自平衡的特点，即左右子树高度几乎一致，所以其查找性能近似于二分查找，时间复杂度是 O(log(n)) 级别；反观链表，它的时间复杂度就不一样了，如果发生了最坏的情况，可能需要遍历整个链表才能找到目标元素，时间复杂度为 O(n)，远远大于红黑树的 O(log(n))，尤其是在节点越来越多的情况下，O(log(n)) 体现出的优势会更加明显。

红黑树的一些其他特点：

- 每个节点要么是红色，要么是黑色，但根节点永远是黑色的。
- 红色节点不能连续，也就是说，红色节点的子和父都不能是红色的。
- 从任一节点到其每个叶子节点的路径都包含相同数量的黑色节点。

正是由于这些规则和要求的限制，红黑树保证了较高的查找效率，所以现在就可以理解为什么 Java 8 的 ConcurrentHashMap 要引入红黑树了。好处就是避免在极端的情况下冲突链表变得很长，在查询的时候，效率会非常慢。而红黑树具有自平衡的特点，所以，即便是极端情况下，也可以保证查询效率在 O(log(n))。

### 分析 Java 8 版本的 ConcurrentHashMap 的重要源码

前面我们讲解了 Java 7 和 Java 8 中 ConcurrentHashMap 的主体结构，下面我们深入源码分析。由于 Java 7 版本已经过时了，所以我们把重点放在 Java 8 版本的源码分析上。

## Node 节点

我们先来看看最基础的内部存储结构 Node，这就是一个一个的节点，如这段代码所示：

```java
static class Node<K,V> implements Map.Entry<K,V> {
    final int hash;
    final K key;
    volatile V val;
    volatile Node<K,V> next;
}
```

可以看出，每个 Node 里面是 key-value 的形式，并且把 value 用 volatile 修饰，以便保证可见性，同时内部还有一个指向下一个节点的 next 指针，方便产生链表结构。

下面我们看两个最重要、最核心的方法。

## put 方法源码分析

put 方法的核心是 putVal 方法，为了方便阅读，我把重要步骤的解读用注释的形式补充在下面的源码中。我们逐步分析这个最重要的方法，这个方法相对有些长，我们一步一步把它看清楚。

```java
//final方法 不允许复写
final V putVal(K key, V value, boolean onlyIfAbsent) {
    if (key == null || value == null) throw new NullPointerException();
    //计算hash值
    int hash = spread(key.hashCode());
    int binCount = 0;
    for (Node<K,V>[] tab = table;;) {
        Node<K,V> f; int n, i, fh; K fk; V fv;
        if (tab == null || (n = tab.length) == 0)
            tab = initTable();
        else if ((f = tabAt(tab, i = (n - 1) & hash)) == null) {
            if (casTabAt(tab, i, null, new Node<K,V>(hash, key, value)))
                break;                   // no lock when adding to empty bin
        }
        else if ((fh = f.hash) == MOVED)
            tab = helpTransfer(tab, f);
        else if (onlyIfAbsent // check first node without acquiring lock
                    && fh == hash
                    && ((fk = f.key) == key || (fk != null && key.equals(fk)))
                    && (fv = f.val) != null)
            return fv;
        else {
            V oldVal = null;
            synchronized (f) {
                if (tabAt(tab, i) == f) {
                    if (fh >= 0) {
                        binCount = 1;
                        for (Node<K,V> e = f;; ++binCount) {
                            K ek;
                            if (e.hash == hash &&
                                ((ek = e.key) == key ||
                                    (ek != null && key.equals(ek)))) {
                                oldVal = e.val;
                                if (!onlyIfAbsent)
                                    e.val = value;
                                break;
                            }
                            Node<K,V> pred = e;
                            if ((e = e.next) == null) {
                                pred.next = new Node<K,V>(hash, key, value);
                                break;
                            }
                        }
                    }
                    else if (f instanceof TreeBin) {
                        Node<K,V> p;
                        binCount = 2;
                        if ((p = ((TreeBin<K,V>)f).putTreeVal(hash, key,
                                                        value)) != null) {
                            oldVal = p.val;
                            if (!onlyIfAbsent)
                                p.val = value;
                        }
                    }
                    else if (f instanceof ReservationNode)
                        throw new IllegalStateException("Recursive update");
                }
            }
            if (binCount != 0) {
                if (binCount >= TREEIFY_THRESHOLD)
                    treeifyBin(tab, i);
                if (oldVal != null)
                    return oldVal;
                break;
            }
        }
    }
    addCount(1L, binCount);
    return null;
}

```

通过以上的源码分析，我们对于 putVal 方法有了详细的认识，可以看出，方法中会逐步根据当前槽点是未初始化、空、扩容、链表、红黑树等不同情况做出不同的处理。

## get 方法源码分析

get 方法比较简单，我们同样用源码注释的方式来分析一下：

```
public&nbsp;V&nbsp;get(Object&nbsp;key)&nbsp;{
&nbsp;&nbsp;&nbsp;&nbsp;Node&lt;K,V&gt;[]&nbsp;tab;&nbsp;Node&lt;K,V&gt;&nbsp;e,&nbsp;p;&nbsp;int&nbsp;n,&nbsp;eh;&nbsp;K&nbsp;ek;
&nbsp;&nbsp;&nbsp;&nbsp;//计算&nbsp;hash&nbsp;值
&nbsp;&nbsp;&nbsp;&nbsp;int&nbsp;h&nbsp;=&nbsp;spread(key.hashCode());
&nbsp;&nbsp;&nbsp;&nbsp;//如果整个数组是空的，或者当前槽点的数据是空的，说明&nbsp;key&nbsp;对应的&nbsp;value&nbsp;不存在，直接返回&nbsp;null
&nbsp;&nbsp;&nbsp;&nbsp;if&nbsp;((tab&nbsp;=&nbsp;table)&nbsp;!=&nbsp;null&nbsp;&amp;&amp;&nbsp;(n&nbsp;=&nbsp;tab.length)&nbsp;&gt;&nbsp;0&nbsp;&amp;&amp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(e&nbsp;=&nbsp;tabAt(tab,&nbsp;(n&nbsp;-&nbsp;1)&nbsp;&amp;&nbsp;h))&nbsp;!=&nbsp;null)&nbsp;{
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//判断头结点是否就是我们需要的节点，如果是则直接返回
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if&nbsp;((eh&nbsp;=&nbsp;e.hash)&nbsp;==&nbsp;h)&nbsp;{
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if&nbsp;((ek&nbsp;=&nbsp;e.key)&nbsp;==&nbsp;key&nbsp;||&nbsp;(ek&nbsp;!=&nbsp;null&nbsp;&amp;&amp;&nbsp;key.equals(ek)))
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return&nbsp;e.val;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//如果头结点&nbsp;hash&nbsp;值小于&nbsp;0，说明是红黑树或者正在扩容，就用对应的&nbsp;find&nbsp;方法来查找
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;else&nbsp;if&nbsp;(eh&nbsp;&lt;&nbsp;0)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return&nbsp;(p&nbsp;=&nbsp;e.find(h,&nbsp;key))&nbsp;!=&nbsp;null&nbsp;?&nbsp;p.val&nbsp;:&nbsp;null;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;//遍历链表来查找
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;while&nbsp;((e&nbsp;=&nbsp;e.next)&nbsp;!=&nbsp;null)&nbsp;{
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if&nbsp;(e.hash&nbsp;==&nbsp;h&nbsp;&amp;&amp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;((ek&nbsp;=&nbsp;e.key)&nbsp;==&nbsp;key&nbsp;||&nbsp;(ek&nbsp;!=&nbsp;null&nbsp;&amp;&amp;&nbsp;key.equals(ek))))
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return&nbsp;e.val;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}
&nbsp;&nbsp;&nbsp;&nbsp;}
&nbsp;&nbsp;&nbsp;&nbsp;return&nbsp;null;
}

```

总结一下 get 的过程：

1. 计算 Hash 值，并由此值找到对应的槽点；
1. 如果数组是空的或者该位置为 null，那么直接返回 null 就可以了；
1. 如果该位置处的节点刚好就是我们需要的，直接返回该节点的值；
1. 如果该位置节点是红黑树或者正在扩容，就用 find 方法继续查找；
1. 否则那就是链表，就进行遍历链表查找。

### 对比Java7 和Java8 的异同和优缺点

## 数据结构

正如本课时最开始的两个结构示意图所示，Java 7 采用 Segment 分段锁来实现，而 Java 8 中的 ConcurrentHashMap 使用数组 + 链表 + 红黑树，在这一点上它们的差别非常大。

<img src="https://s0.lgstatic.com/i/image3/M01/61/21/Cgq2xl4b3kGAVZgMAAG5MQvpc-w153.png" alt="">

<img src="https://s0.lgstatic.com/i/image3/M01/61/21/Cgq2xl4b3l6Ae_CiAAGZw5NzqtE956.png" alt="">

## 并发度

Java 7 中，每个 Segment 独立加锁，最大并发个数就是 Segment 的个数，默认是 16。

但是到了 Java 8 中，锁粒度更细，理想情况下 table 数组元素的个数（也就是数组长度）就是其支持并发的最大个数，并发度比之前有提高。

## 保证并发安全的原理

Java 7 采用 Segment 分段锁来保证安全，而 Segment 是继承自 ReentrantLock。

Java&nbsp;8 中放弃了 Segment 的设计，采用 Node + CAS + synchronized 保证线程安全。

## 遇到 Hash 碰撞

Java 7 在 Hash 冲突时，会使用拉链法，也就是链表的形式。

Java&nbsp;8 先使用拉链法，在链表长度超过一定阈值时，将链表转换为红黑树，来提高查找效率。

## 查询时间复杂度

Java 7 遍历链表的时间复杂度是 O(n)，n 为链表长度。

Java&nbsp;8 如果变成遍历红黑树，那么时间复杂度降低为 O(log(n))，n 为树的节点个数。
