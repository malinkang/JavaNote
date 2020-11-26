## Java8介绍


<h3 id="1.接口默认方法">1.接口默认方法</h3>


Java8 可以通过`default`关键字为接口提供一个非抽象的方法。

```java
interface Formula {
    double calculate(int a);

    default double sqrt(int a) {
        return Math.sqrt(a);
    }
}

```

子类只需要实现抽象方法`calculate`,`sqrt`方法可以被其他方法调用。

```java

Formula formula = new Formula() {
    @Override
    public double calculate(int a) {
        return sqrt(a * 100);
    }
};

formula.calculate(100);     // 100.0
formula.sqrt(16);           // 4.0

```

<h3 id="2.Lambda表达式">2.Lambda表达式</h3>

在以前Java版本中，我们可以通过下面代码实现list的排序

```java

List<String> names = Arrays.asList("peter", "anna", "mike", "xenia");

Collections.sort(names, new Comparator<String>() {
    @Override
    public int compare(String a, String b) {
        return b.compareTo(a);
    }
});

```
Java8提供了一种更简短的语法

```java
Collections.sort(names, (String a, String b) -> {
    return b.compareTo(a);
});

```

如果方法体只有一行，你可以省略`{}`和`return`关键字。java编译器知道参数类型，所以也可以省略参数类型。

```java
Collections.sort(names, (a, b) -> b.compareTo(a));
```

<h3 id="3.Functional接口">3.Functional接口</h3>

我们可以将任意只含一个抽象方法的接口用作lambda表达式。为了确保接口满足需求，应当添加一个`@FunctionalInterface`注解
，当为接口添加两个抽象方法，编译器就会报错。

```java
@FunctionalInterface
interface Converter<F, T> {
    T convert(F from);
}
```

```java

Converter<String, Integer> converter = (from) -> Integer.valueOf(from);
Integer converted = converter.convert("123");
System.out.println(converted);    // 123

```

<h3 id="4.方法和构造函数的引用">4.方法和构造函数的引用</h3>

Java8允许使用`::`关键字传递方法或者构造函数的引用。所以上面的代码可以变成这样

```java

Converter<String, Integer> converter = Integer::valueOf;
Integer converted = converter.convert("123");
System.out.println(converted);   // 123

```
引用对象的方法

```java

class Something {
    String startsWith(String s) {
        return String.valueOf(s.charAt(0));
    }
}

```

```java
Something something = new Something();
Converter<String, String> converter = something::startsWith;
String converted = converter.convert("Java");
System.out.println(converted);    // "J"
```

构造函数引用

```java
class Person {
    String firstName;
    String lastName;

    Person() {}

    Person(String firstName, String lastName) {
        this.firstName = firstName;
        this.lastName = lastName;
    }
}

```

```java

interface PersonFactory<P extends Person> {
    P create(String firstName, String lastName);
}

```

```java
PersonFactory<Person> personFactory = Person::new;
Person person = personFactory.create("Peter", "Parker");
```

Java 编译器会自动选择正确的构造函数通过匹配`PersonFactory.create`的签名。

<h3 id="5.Lambda作用域">5.Lambda作用域</h3>

Lambda访问外部类的变量和匿名内部类非常相似。

读取外部类final修饰的局部变量。

```java
final int num = 1;
Converter<Integer, String> stringConverter =
        (from) -> String.valueOf(from + num);

stringConverter.convert(2);     // 3
```

不同于内部类的是，变量num不一定必须声明为`final`。下面的代码也是可用的。

```java
int num = 1;
Converter<Integer, String> stringConverter =
        (from) -> String.valueOf(from + num);

stringConverter.convert(2);     // 3
```

然后这里的num是暗含的final类型，下面的代码不能通过编译

```java

int num = 1;
Converter<Integer, String> stringConverter =
        (from) -> String.valueOf(from + num);
num = 3;

```
在lambda表达式中也不允许改变num的值。

lambada不允许访问默认方法。下面的代码将不能通过编译。

```java
Formula formula = (a) -> sqrt( a * 100);

```


<h3 id="6.内置Functional接口">6.内置Functional接口</h3>


<h3 id="7.Streams">7.Streams</h3>

Collections在Java 8中被扩展，可以调用`Collection.stream()`或者`Collection.parallelStream()`来创建stream。

首先来创建一个用于操作的集合

```java
List<String> stringCollection = new ArrayList<>();
stringCollection.add("ddd2");
stringCollection.add("aaa2");
stringCollection.add("bbb1");
stringCollection.add("aaa1");
stringCollection.add("bbb3");
stringCollection.add("ccc");
stringCollection.add("bbb2");
stringCollection.add("ddd1");

```

####Filter

```java
stringCollection
    .stream()
    .sorted()
    .filter((s) -> s.startsWith("a"))
    .forEach(System.out::println);

// "aaa1", "aaa2"
```

#### Sorted

```java
stringCollection
    .stream()
    .sorted()
    .filter((s) -> s.startsWith("a"))
    .forEach(System.out::println);

// "aaa1", "aaa2"

```


<h3 id="参考">参考</h3>

* [java8-tutorial](https://github.com/winterbe/java8-tutorial)


