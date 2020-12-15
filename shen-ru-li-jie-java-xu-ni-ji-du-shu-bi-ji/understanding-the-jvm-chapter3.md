# 第3章 垃圾收集器与内存分配策略

## 3.1 概述

## 3.2 对象已死吗

### 3.2.1 引用计数算法

```cpp
public class ReferenceCountingGC {
    public Object instance = null;
    private static final int _1MB = 1024 * 1024;
    private byte[] bigSize = new byte[2*_1MB];
    public static void main(String[] args){
        ReferenceCountingGC objA = new ReferenceCountingGC();
        ReferenceCountingGC objB = new ReferenceCountingGC();
        objA.instance = objB;
        objB.instance = objA;
        objA = null;
        objB = null;
        System.gc();    
    }
}
```

![](https://github.com/malinkang/JavaNote/tree/05f7c6abd740c7af6029fb75682bad60b7d55521/images/understanding-the-jvm/3-1.png)

从运行结果中可以清楚看到，GC日志中包含“4761K-&gt;336K”，意味着虚拟机并没有因为这两个对象互相引用就不回收它们，这也从侧面说明虚拟机并不是通过引用计数算法来判断对象是否存活的。

### 3.2.2 可达性分析算法

在主流的商用程序语言（Java、C\#，甚至包括前面提到的古老的Lisp）的主流实现中，都是称通过可达性分析（Reachability Analysis）来判定对象是否存活的。这个算法的基本思路就是通过一系列的称为“GC Roots”的对象作为起始点，从这些节点开始向下搜索，搜索所走过的路径称为引用链（Reference Chain），当一个对象到GC Roots没有任何引用链相连（用图论的话来说，就是从GC Roots到这个对象不可达）时，则证明此对象是不可用的。如图3-1所示，对象object 5、object 6、object 7虽然互相有关联，但是它们到GC Roots是不可达的，所以它们将会被判定为是可回收的对象。

### 3.2.3 再谈引用

### 3.2.4 生存还是死亡

### 3.2.5 回收方法区

## 3.3 垃圾收集算法

### 3.3.1 标记-清除算法

### 3.3.2 复制算法

### 3.3.3 标记-整理算法

### 3.3.4 分代收集算法

## 3.4 HotSpot的算法实现

### 3.4.1 枚举根节点

### 3.4.2 安全点

### 3.4.3 安全区域

## 3.5 垃圾收集器

### 3.5.1 Serial收集器

### 3.5.2 ParNew收集器

### 3.5.3 Parallel Scavenge收集器

### 3.5.4 Serial Old收集器

### 3.5.5 Parallel Old收集器

### 3.5.6 CMS收集器

### 3.5.7 G1收集器

### 3.5.8 理解GC日志

### 3.5.9 垃圾收集器参数总结

## 3.6 内存分配与回收策略

### 3.6.1 对象优先在Eden分配

### 3.6.2 大对象直接进入老年代

### 3.6.3 长期存活的对象将进入老年代

### 3.6.4 动态对象年龄判定

### 3.6.5 空间分配担保

