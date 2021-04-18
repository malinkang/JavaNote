# Object

`Object`类是`Java`中所有类的基类，在`Java`中每个类都都继承它。但是并不需要这样写：

```java
class Person extends Object
```

如果没有明确地指定基类，`Object`就被认为是这个类的基类。

## equals方法

`Object`类中的`equals`方法用于检测一个对象是否等于另外一个对象。在`Object`类中，这个方法将判断两个对象是否具有相同的引用。如果两个对象具有相同的引用，它们一定是相等的。

