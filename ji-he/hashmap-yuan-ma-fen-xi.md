# HashMap源码分析

## 插入分析

```java
public V put(K key, V value) {
    //调用hash方法
    return putVal(hash(key), key, value, false, true);
}
```



