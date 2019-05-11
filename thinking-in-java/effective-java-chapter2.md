# 第3章 对于所有对象都通用的方法

## 第8条：覆盖equals时请遵守通用约定

在覆盖`equals`方法的时候，你必须要遵守它的通用约定。

* 自反性（reflexive）。对于任何非null的引用值x，`x.equals(x)`必须返回true。

* 对称性（symmetric)。对于任何非null的引用值x和y，当且仅当`y.equals(x)`返回true时，`x.equals(y)`必须返回true。

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