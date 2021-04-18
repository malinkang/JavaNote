# HashMap源码分析



## 查找

```java
public V get(Object key) {
	Node<K,V> e;
	return (e = getNode(hash(key), key)) == null ? null : e.value;
}
```

```java
final Node<K,V> getNode(int hash, Object key) {
    Node<K,V>[] tab; Node<K,V> first, e; int n; K k;
    //数组不为空&数组长度大于0&获取数组的第一个元素不为null
    //定位键值对所在桶的位置
    if ((tab = table) != null && (n = tab.length) > 0 &&
        (first = tab[(n - 1) & hash]) != null) {
        if (first.hash == hash && // always check first node
            ((k = first.key) == key || (key != null && key.equals(k))))
            return first;
        if ((e = first.next) != null) {
            //2.如果first是TreeNode，则调用红黑树查找方法
            if (first instanceof TreeNode)
                return ((TreeNode<K,V>)first).getTreeNode(hash, key);
            do {
               //2.对链表进行查找
                if (e.hash == hash &&
                    ((k = e.key) == key || (key != null && key.equals(k))))
                    return e;
            } while ((e = e.next) != null);
        }
    }
    return null;
}
```

```java
(n - 1) & hash 是对%运算的优化 等价于 hash % n
hash = 185 n = 16 185%16 = 9
	1011 1001
& 0000 1111
------------
  0000 1001 
```



```java
//只有低四位参与位运算冲突几率比较大
//比如169 10101001 与185冲突
//移动四位与得到10101011 则不冲突
static final int hash(Object key) {
  int h;
  return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
}
```

## 遍历

```java
public Set<K> keySet() {
    Set<K> ks = keySet;
    if (ks == null) {
        ks = new KeySet();//创建KeySet对象
        keySet = ks;
    }
    return ks;
}
```

```java
final class KeySet extends AbstractSet<K> {
    public final int size()                 { return size; }
    public final void clear()               { HashMap.this.clear(); }
    public final Iterator<K> iterator()     { return new KeyIterator(); } //创建迭代器
    public final boolean contains(Object o) { return containsKey(o); }
    public final boolean remove(Object key) {
        return removeNode(hash(key), key, null, false, true) != null;
    }
    public final Spliterator<K> spliterator() {
        return new KeySpliterator<>(HashMap.this, 0, -1, 0, 0);
    }
    public final void forEach(Consumer<? super K> action) {
        Node<K,V>[] tab;
        if (action == null)
            throw new NullPointerException();
        if (size > 0 && (tab = table) != null) {
            int mc = modCount;
            for (int i = 0; i < tab.length; ++i) {
                for (Node<K,V> e = tab[i]; e != null; e = e.next)
                    action.accept(e.key);
            }
            if (modCount != mc)
                throw new ConcurrentModificationException();
        }
    }
}
```

```java
abstract class HashIterator {
    Node<K,V> next;        // next entry to return
    Node<K,V> current;     // current entry
    int expectedModCount;  // for fast-fail
    int index;             // current slot

    HashIterator() {
        expectedModCount = modCount;
        Node<K,V>[] t = table;
        current = next = null;
        index = 0;
        if (t != null && size > 0) { // advance to first entry
            //遍历数组找到第一个数组不为空的
            do {} while (index < t.length && (next = t[index++]) == null);
        }
    }

    public final boolean hasNext() {
        return next != null;
    }

    final Node<K,V> nextNode() {
        Node<K,V>[] t;
        Node<K,V> e = next;
        if (modCount != expectedModCount)
            throw new ConcurrentModificationException();
        if (e == null)
            throw new NoSuchElementException();
        //如果走到末尾 寻找下一个数组不为空的
        if ((next = (current = e).next) == null && (t = table) != null) {
            do {} while (index < t.length && (next = t[index++]) == null);
        }
        return e;
    }

    public final void remove() {
        Node<K,V> p = current;
        if (p == null)
            throw new IllegalStateException();
        if (modCount != expectedModCount)
            throw new ConcurrentModificationException();
        current = null;
        K key = p.key;
        removeNode(hash(key), key, null, false, false);
        expectedModCount = modCount;
    }
}
```

```java
final class KeyIterator extends HashIterator
    implements Iterator<K> {
    public final K next() { return nextNode().key; }//
}
```

```java
//两个迭代器都调用的nextNode方法，如果再迭代过程中只需要key的话可以使用keySet遍历
//如果需要value的话则使用EntrySet遍历，如果使用KeySet遍历，则需要调用get方法再次遍历获取
final class EntryIterator extends HashIterator
    implements Iterator<Map.Entry<K,V>> {
    public final Map.Entry<K,V> next() { return nextNode(); } 
}
```





## 插入分析

```java
public V put(K key, V value) {
    //调用hash方法
    return putVal(hash(key), key, value, false, true);
}
```



```java
final V putVal(int hash, K key, V value, boolean onlyIfAbsent,
               boolean evict) {
    Node<K,V>[] tab; Node<K,V> p; int n, i;
    //table延迟到插入数据时才进行初始化
    if ((tab = table) == null || (n = tab.length) == 0)
        n = (tab = resize()).length;
    //如果桶中不包含键值对节点引用，则将新键值对节点的引用插入桶中即可
    //p赋值
    if ((p = tab[i = (n - 1) & hash]) == null)
        tab[i] = newNode(hash, key, value, null);
    else {
        Node<K,V> e; K k;
        // 如果键的值以及节点 hash 等于链表中的第一个键值对节点时，则将 e 指向该键值对
        if (p.hash == hash &&
            ((k = p.key) == key || (key != null && key.equals(k))))
            e = p;
        // 如果桶中的引用类型为 TreeNode，则调用红黑树的插入方法
        else if (p instanceof TreeNode)
            e = ((TreeNode<K,V>)p).putTreeVal(this, tab, hash, key, value);
        else {
            for (int binCount = 0; ; ++binCount) {
                if ((e = p.next) == null) {
                    p.next = newNode(hash, key, value, null);
                    if (binCount >= TREEIFY_THRESHOLD - 1) // -1 for 1st
                        treeifyBin(tab, hash);
                    break;
                }
               // 条件为 true，表示当前链表包含要插入的键值对，终止遍历
              //
                if (e.hash == hash &&
                    ((k = e.key) == key || (key != null && key.equals(k))))
                    break;
                p = e; //e指向的是next p指向e
            }
        }
        if (e != null) { // existing mapping for key
            V oldValue = e.value;
            //onlyIfAbsent 只有是null的时候覆盖，默认是false
            if (!onlyIfAbsent || oldValue == null)
                e.value = value;
            afterNodeAccess(e);
            return oldValue;
        }
    }
    ++modCount;
    if (++size > threshold)
        resize();
    afterNodeInsertion(evict);
    return null;
}
```



```java
final Node<K,V>[] resize() {
  Node<K,V>[] oldTab = table;
  int oldCap = (oldTab == null) ? 0 : oldTab.length;
  int oldThr = threshold;
  int newCap, newThr = 0;
  if (oldCap > 0) {
      if (oldCap >= MAXIMUM_CAPACITY) {
          threshold = Integer.MAX_VALUE;
          return oldTab;
      }
      else if ((newCap = oldCap << 1) < MAXIMUM_CAPACITY &&
               oldCap >= DEFAULT_INITIAL_CAPACITY)
          //新的阈值为老的阈值的两倍
          newThr = oldThr << 1; // double threshold 
  }
  else if (oldThr > 0) // initial capacity was placed in threshold
      newCap = oldThr;
  else {               // zero initial threshold signifies using defaults
      //阈值和容量
      newCap = DEFAULT_INITIAL_CAPACITY;
      newThr = (int)(DEFAULT_LOAD_FACTOR * DEFAULT_INITIAL_CAPACITY);
  }
  if (newThr == 0) {
      float ft = (float)newCap * loadFactor;
      newThr = (newCap < MAXIMUM_CAPACITY && ft < (float)MAXIMUM_CAPACITY ?
                (int)ft : Integer.MAX_VALUE);
  }
  threshold = newThr;
  @SuppressWarnings({"rawtypes","unchecked"})
  Node<K,V>[] newTab = (Node<K,V>[])new Node[newCap];
  table = newTab;
  if (oldTab != null) {
      for (int j = 0; j < oldCap; ++j) {
          Node<K,V> e;
          if ((e = oldTab[j]) != null) {
              oldTab[j] = null;
              if (e.next == null)
                  newTab[e.hash & (newCap - 1)] = e;
              else if (e instanceof TreeNode)
                  ((TreeNode<K,V>)e).split(this, newTab, j, oldCap);
              else { // preserve order
                  Node<K,V> loHead = null, loTail = null;
                  Node<K,V> hiHead = null, hiTail = null;
                  Node<K,V> next;
                  do {
                      next = e.next;
                      if ((e.hash & oldCap) == 0) {
                          if (loTail == null)
                              loHead = e;
                          else
                              loTail.next = e;
                          loTail = e;
                      }
                      else {
                          if (hiTail == null)
                              hiHead = e;
                          else
                              hiTail.next = e;
                          hiTail = e;
                      }
                  } while ((e = next) != null);
                  if (loTail != null) {
                      loTail.next = null;
                      newTab[j] = loHead;
                  }
                  if (hiTail != null) {
                      hiTail.next = null;
                      newTab[j + oldCap] = hiHead;
                  }
              }
          }
      }
  }
  return newTab;
}
```



* [HashMap 源码详细分析(JDK1.8)](http://www.tianxiaobo.com/2018/01/18/HashMap-%E6%BA%90%E7%A0%81%E8%AF%A6%E7%BB%86%E5%88%86%E6%9E%90-JDK1-8/)

* [Java 8系列之重新认识HashMap](https://tech.meituan.com/2016/06/24/java-hashmap.html)
* [《吊打面试官》系列-HashMap](https://mp.weixin.qq.com/s/0Gf2DzuzgEx0i3mHVvhKNQ)

