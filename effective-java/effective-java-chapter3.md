---
title: 《Effective Java》读书笔记 第3章 对于所有对象都通用的方法
date: '2019-02-12T09:54:13.000Z'
tags:
  - Java
  - 读书笔记
toc: true
---

# 第3章 对于所有对象都通用的方法

## 第8条：覆盖equals时请遵守通用约定

在覆盖`equals`方法的时候，你必须要遵守它的通用约定。

* 自反性（reflexive）。对于任何非null的引用值x，`x.equals(x)`必须返回true。
* 对称性（symmetric\)。对于任何非null的引用值x和y，当且仅当`y.equals(x)`返回true时，`x.equals(y)`必须返回true。
* 传递性（transitive）。对于任何非null的引用值x、y和z，如果`x.equals(y)`返回true，并且`y.equals(z)`也返回true，那么`x.equals(z)`也必须返回true。
* 一致性（consistent）。对于任何非null的引用值x和y，只要`equals`的比较操作再对象中所用的信息没有被修改，多次调用`x.equals(y)`就会一致地返回true，或者一致地返回false。
* 对于任何非null的引用值x，`x.equals(null)`必须返回false。

```java
public class CaseInsensitiveString {
    private final String s;
    public CaseInsensitiveString(String s){
        if(s==null)
            throw new NullPointerException();
        this.s = s;
    }

    @Override
    public boolean equals(Object obj) {
        if(obj instanceof CaseInsensitiveString)
            return s.equalsIgnoreCase(((CaseInsensitiveString) obj).s);
        if(obj instanceof String)
            return s.equalsIgnoreCase((String) obj);
        return false;
    }
}
```

```java
CaseInsensitiveString cis = new CaseInsensitiveString("Polish");
String s = "polish";
//违反了对称性
System.out.println(cis.equals(s)); //true
System.out.println(s.equals(cis)); //false
```

一旦违反了`equals`约定，当其他对象面对你的对象时，你完全不知道这些对象的行为会怎么样。

为了解决这个问题，只需把企图与`String`互操作的这段代码从`equals`方法中去掉就可以了。

```java
@Override
public boolean equals(Object obj) {
    return obj instanceof CaseInsensitiveString
        && s.equalsIgnoreCase(((CaseInsensitiveString) obj).s);
}
```

```java
public class Point {
    private final int x;
    private final int y;

    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    @Override
    public boolean equals(Object obj) {
        if (!(obj instanceof Point))
            return false;
        Point point = (Point) obj;
        return point.x == x && point.y == y;
    }
}
```

扩展这个类，为一个点添加颜色信息：

```java
public class ColorPoint extends Point {
    private final Color color;

    public ColorPoint(int x, int y, Color color) {
        super(x, y);
        this.color = color;
    }
}
```

如果完全不提供`equals`方法，而是直接从`Point`继承过来，在`equals`做比较的时候颜色信息就被忽略掉了。编写一个`equals`方法，只有当它的参数是另一个有色点，并且具有同样的位置和颜色时，它才会返回`true`:

```java
@Override
public boolean equals(Object obj) {
    if (!(obj instanceof ColorPoint))
        return false;
    return super.equals(obj) && ((ColorPoint) obj).color == color;
}
```

这个方法的问题在于，你在比较普通点和有色点，以及相反的情形时，可能会得到不同的结果。前一种比较忽略了颜色信息，而后一种比较则总是返回`false`，因为参数的类型不正确。

```java
Point p = new Point(1, 2);
ColorPoint cp = new ColorPoint(1, 2, Color.RED);
System.out.println(p.equals(cp)); // true
System.out.println(cp.equals(p)); // false
```

可以做这样的尝试来修正这个问题，让`ColorPoint.equals`在进行“混合比较”时忽略颜色信息。

```java
@Override
public boolean equals(Object obj) {
    if (!(obj instanceof Point))
        return false;
    if (!(obj instanceof ColorPoint))
        return obj.equals(this);
    return super.equals(obj) && ((ColorPoint) obj).color == color;
}
```

这种方法确实提供了对称性，但是却牺牲了传递性：

```java
ColorPoint p1 = new ColorPoint(1, 2, Color.RED);
Point p2 = new Point(1, 2);
ColorPoint p3 = new ColorPoint(1, 2, Color.BLUE);
System.out.println(p1.equals(p2));  // true
System.out.println(p2.equals(p3));  // true
System.out.println(p1.equals(p3));  // false
```

怎么解决呢？事实上，这是面向对象语言中关于等价关系的一个基本问题。我们**无法在扩展可实例化的类的同时，既增加新的值组件，同时又保留`equals`约定，**除非愿意放弃面向对象的抽象所带来的优势。

在`equals`方法中用`getClass`测试替代`instanceof`测试，可以扩展可实例化的类和增加新的值组件，同时保留`equals`约定：

```java
@Override
public boolean equals(Object obj) {
    if (obj == null || obj.getClass() != getClass())
        return false;
    Point p = (Point) obj;
    return p.x == x && p.y == y;
}
```

这段程序只有当对象具有相同的实现时，才能使对象等同。

虽然没有一种令人满意的方法可以既扩展不可实例化的类，又增加值组件，但还是有一种不错的权宜之计。根据第16条建议：复合优先于继承。我们不再让`ColorPoint`扩展`Point`，而是在`ColorPoint`中加入一个私有的`Point`域，以及一个公有的视图方法，此方法返回一个与该有色点处于相同位置的普通`Point`对象。

```java
public class ColorPoint {
    private final Point point;
    private final Color color;

    public ColorPoint(int x, int y, Color color) {
        if (color == null)
            throw new NullPointerException();
        point = new Point(x, y);
        this.color = color;
    }

    public Point asPoint() {
        return point;
    }

    @Override
    public boolean equals(Object obj) {
        if (!(obj instanceof ColorPoint))
            return false;
        ColorPoint cp = (ColorPoint) obj;
        return cp.point.equals(point) && cp.color.equals(color);
    }
}
```

结合所有这些要求，得出了以下实现高质量`equals`方法的诀窍：

1. 使用==操作符检查“参数是否为这个对象的引用”。
2. 使用`instanceof`操作符检查“参数是否为正确的类型”。
3. 把参数转换成正确的类型。
4. 对于该类中的每个“关键”域，检查参数中的域是否与该对象中对应的域相匹配。
5. 当编写完成了equals方法之后，应该问自己三个问题：它是否是对称的、传递的、一致的？

下面是最后的告诫：

* 覆盖equals时总要覆盖hashCode。
* 不要企图让`equals`方法过于智能。
* 不要让equals声明中的Object对象替换为其他的类型。

## 第9条：覆盖equals时总要覆盖hashCode

一个很常见的错误根源在于没有覆盖`hashCode`方法。在每个覆盖了equals方法的类中，也必须覆盖hashCode方法。如果不这样做的话，就会违法`hashCode`的通用约定，从而导致该类无法结合所有基于散列的集合一起正常运作，这样的集合包括`HashMap`、`HashSet`和`Hashtable`。

下面是约定的内容，摘自`Object`规范。

* 在应用程序的执行期间，只要对象的`equals`方法的比较操作所用到的信息没有被修改，那么对这同一个对象调用多次，`hashCode`方法都必须始终如一地返回同一个整数。在同一个应用程序的多次执行过程中，每次执行所返回的整数可以不一致。
* 如果两个对象根据`equals（Object）`方法比较是相等的，那么调用这两个对象中任意一个对象的`hashCode`方法都必须产生同样的整数结果。
* 如果两个对象根据`equals`方法比较是不相等的，那么调用这两个对象任意一个对象的`hashCode`方法，则不一定要产生不同的整数结果。但程序员应该知道，给不相等的对象产生截然不同的整数结果，有可能提高散列表的性能。

```java
public final class PhoneNumber {
    private final short areaCode;
    private final short prefix;
    private final short lineNumber;

    public PhoneNumber(int areaCode, int prefix, int lineNumber) {
        rangeCheck(areaCode, 999, "area code");
        rangeCheck(prefix, 999, "prefix");
        rangeCheck(lineNumber, 9999, "lineNumber");
        this.areaCode = (short) areaCode;
        this.prefix = (short) prefix;
        this.lineNumber = (short) lineNumber;
    }

    private static void rangeCheck(int arg, int max, String name) {
        if (arg < 0 || arg > max)
            throw new IllegalArgumentException(name + ":" + arg);
    }
}
```

```java
Map<PhoneNumber, String> m = new HashMap<>();
m.put(new PhoneNumber(707, 867, 5309), "Jenny");
System.out.println(m.get(new PhoneNumber(707, 867, 5309))); // null
```

一个好的散列函数通常倾向于“为不相等的对象产生不相等的散列码”。这正是`hashCode`约定中第三条的含义。理想情况下，散列函数应该把集合中不相等的实例均匀地分布到所有可能的散列值上。要想完全达到这种理想的情形是非常困难的。幸运的是，相对接近这种理想情形则并不太困难。下面给出一种简单的解决方法：

1. 把某个非零的常数值，比如说17，保存在一个名为`result`的`int`类型的变量中。
2. 对于对象中每个关键域f，完成以下步骤：
   1. 为该域计算int类型的散列码
      1. 如果该域是boolean类型，则计算（f?1:0）。
      2. 如果该域是byte、char、short或者int类型，则计算\(int\)f。
      3. 如果该域是long类型，则计算\(int\)\(f^\(f&gt;&gt;&gt;32\)\)。
      4. 如果该域是float类型，则计算`Float.floatToIntBits(f)`。
      5. 如果该域是double类型，则计算`Double.doubleToLongBits(f)`，然后为得到的long类型计算散列值。
      6. 如果该域是一个对象引用，并且该类的`equals`方法通过递归地调用`equals`的方法来比较这个域，则同样为这个域递归地调用`hashCode`。如果需要更复杂的比较，则为这个域计算一个`范式`，然后针对这个范式调用`hashCode`。如果这个域的值为null，则返回0。
      7. 如果该域是一个数组，则要把每一个元素当做单独的域来处理。也就是说，递归地应用上述规则，对每个重要的元素计算一个散列码，然后根据步骤2.2中的做法把这些散列值组合起来。如果数组域中的每个元素都很重要，可以利用发型版本1.5中增加的其中一个`Arrays.hashCode`方法。
   2. 按照下面的公式，把步骤2.1中计算得到的散列码c合并到result中：

      `result = 31 * result + c`;
3. 返回result
4. 写完hashCode方法之后，问问自己“相等的实例是否具有相等的散列码”。要编写单元测试来验证你的推断。如果相等的实例有着不相等的散列码，则要找出原因，并修正错误。

## 第10条：始终要覆盖toString

## 第11条：谨慎地覆盖clone

## 第12条：考虑实现Comparable接口

