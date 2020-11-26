# 集合

## 目录

* [2.List](ji-he.md#2.List)
  * [2.1ArrayList](ji-he.md#2.1ArrayList)
    * [2.1.1构造方法](ji-he.md#2.1.1构造方法)
    * [2.1.2添加元素](ji-he.md#2.1.2添加元素)
    * [2.1.3获取](ji-he.md#2.1.3获取)
    * [2.1.4删除](ji-he.md#2.1.4删除)
    * [2.1.5其他常用方法](ji-he.md#2.1.5其他常用方法)
  * [2.2LinkedList](ji-he.md#2.2LinkedList)
    * [2.2.1构造函数](ji-he.md#2.2.1构造函数)
    * [2.2.2添加](ji-he.md#2.2.2添加)
    * [2.2.3删除](ji-he.md#2.2.3删除)
    * [2.2.4获取](ji-he.md#2.2.4获取)
  * [2.3Vector](ji-he.md#2.3Vector)
  * [2.4Stack](ji-he.md#2.4Stack)
* [3.Set](ji-he.md#3.Set)
  * [3.1HashSet](ji-he.md#3.1HashSet)
  * [3.2TreeSet](ji-he.md#3.2TreeSet)
* [参考](ji-he.md#参考)

集合的整体框架

![](.gitbook/assets/collection.jpg)

## 2.List <a id="2.List"></a>

List是一个继承于Collection的接口，即List是集合中的一种。List是有序的队列，List中的每一个元素都有一个索引；第一个元素的索引值是0，往后的元素的索引值依次+1。和Set不同，List中允许有重复的元素。

### 2.1ArrayList <a id="2.1ArrayList"></a>

ArrayList实现List接口，底层使用数组保存所有的元素。其操作基本上是对数组的操作。

#### 2.1.1构造方法 <a id="2.1.1&#x6784;&#x9020;&#x65B9;&#x6CD5;"></a>

```java
   public ArrayList() {
        this.elementData = DEFAULTCAPACITY_EMPTY_ELEMENTDATA;
    }

    //创建指定容量的List
    public ArrayList(int initialCapacity) {
        if (initialCapacity > 0) {
            this.elementData = new Object[initialCapacity];
        } else if (initialCapacity == 0) {
            this.elementData = EMPTY_ELEMENTDATA;
        } else {
            throw new IllegalArgumentException("Illegal Capacity: "+
                                               initialCapacity);
        }
    }

    public ArrayList(Collection<? extends E> c) {
        elementData = c.toArray();
        if ((size = elementData.length) != 0) {
            // c.toArray might (incorrectly) not return Object[] (see 6260652)
            if (elementData.getClass() != Object[].class)
                elementData = Arrays.copyOf(elementData, size, Object[].class);
        } else {
            // replace with empty array.
            this.elementData = EMPTY_ELEMENTDATA;
        }
    }
```

#### 2.1.2添加元素 <a id="2.1.2&#x6DFB;&#x52A0;&#x5143;&#x7D20;"></a>

ArrayList提供了下列方法进行添加元素。

* public E set\(int index, E element\) 

```java
//用指定的元素替代此列表中指定位置上的元素，并返回以前位于该位置上的元素。
    public E set(int index, E element) {
        rangeCheck(index);

        E oldValue = elementData(index);
        elementData[index] = element;
        return oldValue;
    }

    E elementData(int index) {
        return (E) elementData[index];
    }
```

* public boolean add\(E e\)

```java
//将指定的元素添加到此列表的末尾
    public boolean add(E e) {
        ensureCapacityInternal(size + 1);  // Increments modCount!!
        elementData[size++] = e;
        return true;
    }
```

* public void add\(int index, E element\)

```java
// 将指定的元素插入此列表中的指定位置。
// 如果当前位置有元素，则向右移动当前位于该位置的元素以及所有后续元素（将其索引加1）。
public void add(int index, E element) {
    if (index > size || index < 0)
        throw new IndexOutOfBoundsException("Index: "+index+", Size: "+size);
    // 如果数组长度不足，将进行扩容。
    ensureCapacity(size+1);  // Increments modCount!!
    // 将 elementData中从Index位置开始、长度为size-index的元素，
    // 拷贝到从下标为index+1位置开始的新的elementData数组中。
    // 即将当前位于该位置的元素以及所有后续元素右移一个位置。
    System.arraycopy(elementData, index, elementData, index + 1, size - index);
    elementData[index] = element;
    size++;
}
```

System提供的静态方法`arraycopy()`,我们可以使用它来实现数组之间的复制。

方法签名public static native void arraycopy\(Object src, int srcPos, Object dest, int destPos, int length\);

* src:源数组
* srcPos:源数组要复制的起始位置
* dest:目标数组
* destPos:目标数组放置的起始位置，
* length：复制的长度

  ```java
        int[] array1={1,2,3,4,5,6};
        int [] array2= {5,4,3,2,1};
        System.arraycopy(array1,0,array2,1,2);

        for (int i = 0; i < array2.length; i++) {
            System.out.println(array2[i]);
        }
  //        5
  //        1
  //        2
  //        2
  //        1
  ```

  这个函数也可以实现自己到自己的复制。

  ```java
        int[] array1={1,2,3,4,5,6};
        System.arraycopy(array1,0,array1,3,3);

        for (int i = 0; i < array1.length; i++) {
            System.out.println(array1[i]);
        }
  //        1
  //        2
  //        3
  //        1
  //        2
  //        3
  ```

```java
// 按照指定collection的迭代器所返回的元素顺序，将该collection中的所有元素添加到此列表的尾部。
public boolean addAll(Collection<? extends E> c) {
    Object[] a = c.toArray();
    int numNew = a.length;
    ensureCapacity(size + numNew);  // Increments modCount
    System.arraycopy(a, 0, elementData, size, numNew);
    size += numNew;
    return numNew != 0;
}
```

#### 2.1.3获取 <a id="2.1.3&#x83B7;&#x53D6;"></a>

```java
// 返回此列表中指定位置上的元素。
public E get(int index) {
    RangeCheck(index);

    return (E) elementData[index];
}
```

#### 2.1.4删除 <a id="2.1.4&#x5220;&#x9664;"></a>

ArrayList提供了根据下标或者指定对象两种方式的删除功能。

```java
// 移除此列表中指定位置上的元素。返回删除的元素
public E remove(int index) {
    RangeCheck(index);

    modCount++;
    E oldValue = (E) elementData[index];

    int numMoved = size - index - 1;
    if (numMoved > 0)
        System.arraycopy(elementData, index+1, elementData, index, numMoved);
    elementData[--size] = null; // Let gc do its work

    return oldValue;
}
```

```java
// 移除此列表中首次出现的指定元素（如果存在）。这是应为ArrayList中允许存放重复的元素。
public boolean remove(Object o) {
    // 由于ArrayList中允许存放null，因此下面通过两种情况来分别处理。
    if (o == null) {
        for (int index = 0; index < size; index++)
            if (elementData[index] == null) {
                // 类似remove(int index)，移除列表中指定位置上的元素。
                fastRemove(index);
                return true;
            }
} else {
    for (int index = 0; index < size; index++)
        if (o.equals(elementData[index])) {
            fastRemove(index);
            return true;
        }
    }
    return false;
}
```

#### 2.1.5其他常用方法 <a id="2.1.5&#x5176;&#x4ED6;&#x5E38;&#x7528;&#x65B9;&#x6CD5;"></a>

* public int indexOf\(Object o\)

  ```java
  //返回指定元素第一次出现的索引，如果没有该元素返回-1
   public int indexOf(Object o) {
       if (o == null) {
           for (int i = 0; i < size; i++)
               if (elementData[i]==null)
                   return i;
       } else {
           for (int i = 0; i < size; i++)
               if (o.equals(elementData[i]))
                   return i;
       }
       return -1;
   }
  ```

* public int lastIndexOf\(Object o\)

```java
//返回指定元素最后一次出现的索引，如果不存在该元素返回-1
public int lastIndexOf(Object o) {
        if (o == null) {
            for (int i = size-1; i >= 0; i--)
                if (elementData[i]==null)
                    return i;
        } else {
            for (int i = size-1; i >= 0; i--)
                if (o.equals(elementData[i]))
                    return i;
        }
        return -1;
    }
```

* public Object\[\] toArray\(\)

```java
//将ArrayList转换为数组
    public Object[] toArray() {
        return Arrays.copyOf(elementData, size);
    }
```

* public  T\[\] toArray\(T\[\] a\)

  ```java
    public <T> T[] toArray(T[] a) {
        if (a.length < size)
        //当数组长度小于集合长度创建一个新的数组，并且复制集合里的所有元素
            // Make a new array of a's runtime type, but my contents:
            return (T[]) Arrays.copyOf(elementData, size, a.getClass());
        //当数组长度大于等于集合长度，将集合中的所有元素复制到集合里
        System.arraycopy(elementData, 0, a, 0, size);
        if (a.length > size)
            a[size] = null;
        return a;
    }
  ```

* public void clear\(\)

```java
//清除所有元素
    public void clear() {
        modCount++;

        // clear to let GC do its work
        for (int i = 0; i < size; i++)
            elementData[i] = null;

        size = 0;
    }
```

#### 2.1.6遍历 <a id="2.1.6&#x904D;&#x5386;"></a>

遍历可以通过for循环，foreach循环，Iterator和ListIterator四种方式进行遍历。

在foreach循环和iterator调用ArrayList的add和remove方法将会出现`ConcurrentModificationException`异常。所以要想遍历的时候修改集合，只能使用for循环，或者使用Iterator的remove方法。

### 2.2LinkedList <a id="2.2LinkedList"></a>

LinkedList是基于[链表](https://zh.wikipedia.org/wiki/%E9%93%BE%E8%A1%A8)的集合，其查询速度肯定比不上基于数组实现的集合。但是链表实现的最大优点在于，频繁的操作节点速度就比较快。

LinkedList内部有一个静态的内部类Node，代表节点。

```java
  private static class Node<E> {
        E item;//元素
        Node<E> next;//下一个节点
        Node<E> prev;//上一个节点

        Node(Node<E> prev, E element, Node<E> next) {
            this.item = element;
            this.next = next;
            this.prev = prev;
        }
    }
```

#### 2.2.1构造函数 <a id="2.2.1&#x6784;&#x9020;&#x51FD;&#x6570;"></a>

```java
    public LinkedList() {
    }
public LinkedList(Collection<? extends E> c) {
        this();
        addAll(c);
    }
      public boolean addAll(Collection<? extends E> c) {
        return addAll(size, c);
    }
     public boolean addAll(int index, Collection<? extends E> c) {
        checkPositionIndex(index);

        Object[] a = c.toArray();
        int numNew = a.length;
        if (numNew == 0)
            return false;

        Node<E> pred, succ;
        if (index == size) {
            succ = null;
            pred = last;
        } else {
            succ = node(index);
            pred = succ.prev;
        }

        for (Object o : a) {
            @SuppressWarnings("unchecked") E e = (E) o;
            Node<E> newNode = new Node<>(pred, e, null);
            if (pred == null)
                first = newNode;
            else
                pred.next = newNode;
            pred = newNode;
        }

        if (succ == null) {
            last = pred;
        } else {
            pred.next = succ;
            succ.prev = pred;
        }

        size += numNew;
        modCount++;
        return true;
    }
```

#### 2.2.2添加 <a id="2.2.2&#x6DFB;&#x52A0;"></a>

```java
//添加指定元素到末尾
 public boolean add(E e) {
        linkLast(e);
        return true;
    }
```

```java
//在末尾添加节点
   void linkLast(E e) {
        final Node<E> l = last;
        final Node<E> newNode = new Node<>(l, e, null);
        last = newNode;
        if (l == null)
            first = newNode;
        else
            l.next = newNode;
        size++;
        modCount++;
    }
```

```java
//添加指定元素到指定位置
  public void add(int index, E element) {
        checkPositionIndex(index);

        if (index == size)
            linkLast(element);
        else
            linkBefore(element, node(index));
    }
```

```java
//根据索引返回节点
Node<E> node(int index) {
        // assert isElementIndex(index);

        if (index < (size >> 1)) {
            Node<E> x = first;
            for (int i = 0; i < index; i++)
                x = x.next;
            return x;
        } else {
            Node<E> x = last;
            for (int i = size - 1; i > index; i--)
                x = x.prev;
            return x;
        }
    }
```

```java
//指定节点前插入元素
void linkBefore(E e, Node<E> succ) {
        // assert succ != null;
        final Node<E> pred = succ.prev;
        final Node<E> newNode = new Node<>(pred, e, succ);
        succ.prev = newNode;
        if (pred == null)
            first = newNode;
        else
            pred.next = newNode;
        size++;
        modCount++;
    }
```

```java
//在开始位置插入指定元素
  public void addFirst(E e) {
        linkFirst(e);
    }
```

```java
//在末尾插入指定元素
public void addLast(E e) {
        linkLast(e);
    }
```

#### 2.2.3删除 <a id="2.2.3&#x5220;&#x9664;"></a>

* public E remove\(\)：删除第一个元素

```java
   public E remove() {
        return removeFirst();
    }
```

* public E remove\(int index\)：删除指定位置的元素

```java
    public E remove(int index) {
        checkElementIndex(index);
        return unlink(node(index));
    }
```

* public E remove\(int index\)：删除指定位置的元素

```java
    public E remove(int index) {
        checkElementIndex(index);
        return unlink(node(index));
    }
```

* public boolean remove\(Object o\)：删除指定元素首次出现的该元素

```java
    public boolean remove(Object o) {
        if (o == null) {
            for (Node<E> x = first; x != null; x = x.next) {
                if (x.item == null) {
                    unlink(x);
                    return true;
                }
            }
        } else {
            for (Node<E> x = first; x != null; x = x.next) {
                if (o.equals(x.item)) {
                    unlink(x);
                    return true;
                }
            }
        }
        return false;
    }
```

* public boolean remove\(Object o\)：删除指定元素首次出现的该元素

```java
    public boolean remove(Object o) {
        if (o == null) {
            for (Node<E> x = first; x != null; x = x.next) {
                if (x.item == null) {
                    unlink(x);
                    return true;
                }
            }
        } else {
            for (Node<E> x = first; x != null; x = x.next) {
                if (o.equals(x.item)) {
                    unlink(x);
                    return true;
                }
            }
        }
        return false;
    }
```

* public E removeFirst\(\) ：删除第一个
* public E removeLast\(\)：删除最后一个
* public E poll\(\)：删除第一个
* public E pollFirst\(\) ：删除第一个
* public E pollLast\(\)：删除第一个

#### 2.2.4获取 <a id="2.2.4&#x83B7;&#x53D6;"></a>

* public E get\(int index\)：根据索引获取
* public E getLast\(\)：获取最后一个
* public E getFirst\(\)：获取第一个
* public E peek\(\)：获取第一个
* public E peekFirst\(\) ：获取第一个
* public E peekLast\(\)：获取最后一个

### 2.3Vector <a id="2.3Vector"></a>

`Vector`也是基于数组实现的队列，代码和ArrayList非常相似，只不过Vector是线程同步，其执行的效率相比ArrayList就低了。

### 2.4Stack <a id="2.4Stack"></a>

`Stack`是栈。它的特性是：先进后出\(FILO, First In Last Out\)。Stack是继承于Vector\(矢量队列\)的，由于Vector是通过数组实现的，这就意味着，Stack也是通过数组实现的。

## 3.Set <a id="3.Set"></a>

Set是一个继承于Collection的接口，即Set也是集合中的一种。Set是没有重复元素的集合。

### 3.1HashSet <a id="3.1HashSet"></a>

HashSet依赖于HashMap,它实际上是通过HashMap实现的。HashSet中的元素是无序的。

### 3.2TreeSet <a id="3.2TreeSet"></a>

TreeSet依赖于TreeMap，它实际上是通过TreeMap实现的。TreeSet中的元素是有序的。

## 参考 <a id="&#x53C2;&#x8003;"></a>

* [深入Java集合学习系列：ArrayList的实现原理](http://zhangshixi.iteye.com/blog/674856)

