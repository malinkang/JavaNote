# final 

## final修饰变量

变量可以分为以下三种:
成员变量，类中的非 static 修饰的属性; 静态变量，类中的被 static 修饰的属性; 局部变量，方法中的变量。

### 成员变量

成员变量指的是一个类中的非 static 属性，对于这种成员变量而言，被 final 修饰后，它有三种赋值时机(或者叫作赋值途 径)。

* 第一种是在声明变量的等号右边直接赋值，例如:

```java
public class FinalFieldAssignment1 { private final int finalVar = 0;
}
```
在这个类中有 “private final int finalVar = 0” ，这就是在声明变量的时候就已经赋值了。

* 第二种是在构造函数中赋值，例如:

```java
class FinalFieldAssignment2 { 
    private final int finalVar;
    public FinalFieldAssignment2() { 
        finalVar = 0;
    } 
}
```
在这个例子中，我们首先声明了变量，即 private final int finalVar，且没有把它赋值，然后在这个类的构造函数中对它进行赋 值，这也是可以的。


* 第三种就是在类的构造代码块中赋值(不常用)，例如:

```java
class FinalFieldAssignment3 { 
    private final int finalVar;
    {
        finalVar = 0;
    } 
}
```

我们同样也声明了一个变量 private final int finalVar，且没有把它赋值，然后在下面的一个由大括号括起来的类的构造代码块 中，对变量进行了赋值，这也是合理的赋值时机。
需要注意的是，这里讲了三种赋值时机，我们必须从中挑一种来完成对 final 变量的赋值。如果不是 final 的普通变量，当然可 以不用在这三种情况下赋值，完全可以在其他的时机赋值;或者如果你不准备使用这个变量，那么自始至终不赋值甚至也是可 以的。但是对于 final 修饰的成员变量而言，必须在三种情况中任选一种来进行赋值，而不能一种都不挑、完全不赋值，那是 不行的，这是 final 语法所规定的。

* 空白 final

下面讲解一种概念:“空白 final”。如果我们声明了 final 变量之后，并没有立刻在等号右侧对它赋值，这种情况就被称为“空白 final”。这样做的好处在于增加了 final 变量的灵活性，比如可以在构造函数中根据不同的情况，对 final 变量进行不同的赋值， 这样的话，被 final 修饰的变量就不会变得死板，同时又能保证在赋值后保持不变。我们用下面这个代码来说明:

```java
/**
* 描述: 空白final提供了灵活性 */
public class BlankFinal {
//空白final
    private final int a;
        //不传参则把a赋值为默认值0 public BlankFinal() {
        this.a = 0; 
    }
        //传参则把a赋值为传入的参数 
    public BlankFinal(int a) {
        this.a = a; 
    }
}
```
在这个代码中，我们有一个 private final 的 int 变量叫作 a，该类有两个构造函数，第一个构造函数是把 a 赋值为 0，第二个构 造函数是把 a 赋值为传进来的参数，所以你调用不同的构造函数，就会有不同的赋值情况。这样一来，利用这个规则，我们就 可以根据业务去给 final 变量设计更灵活的赋值逻辑。所以利用空白 final 的一大好处，就是可以让这个 final 变量的值并不是说 非常死板，不是绝对固定的，而是可以根据情况进行灵活的赋值，只不过一旦赋值后，就不能再更改了。

### 静态变量

静态变量是类中的 static 属性，它被 final 修饰后，只有两种赋值时机。


* 第一种同样是在声明变量的等号右边直接赋值，例如:

```java
public class StaticFieldAssignment1 { 
    private static final int a = 0;
}
```
第二种赋值时机就是它可以在一个静态的 static 初始代码块中赋值，例如:

```java
class StaticFieldAssignment2 {
    private static final int a;
    static {
        a = 0;
    } 
}
```
在这个类中有一个变量 private static final int a，然后有一个 static，接着是大括号，这是静态初始代码块的语法，在这里面我们 对 a 进行了赋值，这种赋值时机也是允许的。以上就是静态 final 变量的两种赋值时机。

需要注意的是，我们不能用普通的非静态初始代码块来给静态的 final 变量赋值。同样有一点比较特殊的是，这个 static 的 final 变量不能在构造函数中进行赋值。

### 局部变量

局部变量指的是方法中的变量，如果你把它修饰为了 final，它的含义依然是一旦赋值就不能改变。
但是它的赋值时机和前两种变量是不一样的，因为它是在方法中定义的，所以它没有构造函数，也同样不存在初始代码块，所 以对应的这两种赋值时机就都不存在了。实际上，对于 final 的局部变量而言，它是不限定具体赋值时机的，只要求我们在使 用之前必须对它进行赋值即可。
这个要求和方法中的非 final 变量的要求也是一样的，对于方法中的一个非 final 修饰的普通变量而言，它其实也是要求在使用 这个变量之前对它赋值。我们来看下面这个代码的例子:

```java
/**
* 描述: 本地变量的赋值时机:使用前赋值即可 */
public class LocalVarAssignment1 {
    public void foo() {
        final int a = 0;//等号右边直接赋值 
    }
}
class LocalVarAssignment2 {
    public void foo() {
        final int a;//这是允许的，因为a没有被使用 
    }
}
class LocalVarAssignment3 {
    public void foo() { 
        final int a;
        a = 0;//使用前赋值
        System.out.println(a); 
    }
}
```

首先我们来看下第一个类，即 LocalVarAssignment1，然后在 foo() 方法中有一个 final 修饰的 int a，最后这里直接在等号右边 赋值。
下面看第二个类，由于我们后期没有使用到这个 final 修饰的局部变量 a，所以这里实际上自始至终都没有对 a 进行赋值，即便 它是 final 的，也可以对它不赋值，这种行为是语法所允许的。
第三种情况就是先创造出一个 final int a，并且不在等号右边对它进行赋值，然后在使用之前对 a 进行赋值，最后再使用它，这 也是允许的。
总结一下，对于这种局部变量的 final 变量而言，它的赋值时机就是要求在使用之前进行赋值，否则使用一个未赋值的变量， 自然会报错。


### final 修饰参数

关键字 final 还可以用于修饰方法中的参数。在方法的参数列表中是可以把参数声明为 final 的，这意味着我们没有办法在方法
内部对这个参数进行修改。例如:

在这个代码中有一个 withFinal 方法，而且这个方法的入参 a 是被 final 修饰的。接下来，我们首先把入参的 a 打印出来，这是 允许的，意味着我们可以读取到它的值;但是接下来我们假设想在方法中对这个 a 进行修改，比如改成 a = 9，这就会报编译 错误，因此不允许修改 final 参数的值。

```java
public class FinalPara {
    public void withFinal(final int a){
        System.out.println(a);
//        a = 9; 编译错误，不允许修改
    }
}
```


## final修饰方法

下面来看一看 final 修饰方法的情况。选择用 final 修饰方法的原因之一是为了提高效率，因为在早期的 Java 版本中，会把 final 方法转为内嵌调用，可以消除方法调用的开销，以提高程序的运行效率。不过在后期的 Java 版本中，JVM 会对此自动进行优 化，所以不需要我们程序员去使用 final 修饰方法来进行这些优化了，即便使用也不会带来性能上的提升。


目前我们使用 final 去修饰方法的唯一原因，就是想把这个方法锁定，意味着任何继承类都不能修改这个方法的含义，也就是 说，被 final 修饰的方法不可以被重写，不能被 override。我们来举一个代码的例子:

```java
public class FinalMethod {
    public void drink(){
    }
    public final void eat(){
    }
}
public class SubClass extends FinalMethod{
    @Override
    public void drink() {
        super.drink();
    }
    //编译错误
//    public void eat(){
//
//    }
}
```
## final修饰类

final 修饰类的含义很明确，就是这个类“不可被继承”。

```java
final public class FinalClassDemo {
}
////编译错误，无法继承final的类
//public class A extends FinalClassDemo{
//}
```

有一个 final 修饰的类叫作 FinalClassDemo，然后尝试写 class A extends FinalClassDemo，结果会报编译错误，因为语法规定无 法继承 final 类，那么我们给类加上 final 的目的是什么呢?如果我们这样设计，就代表不但我们自己不会继承这个类，也不允 许其他人来继承，它就不可能有子类的出现，这在一定程度上可以保证线程安全。
比如非常经典的 String 类就是被 final 修饰的，所以我们自始至终也没有看到过哪个类是继承自 String 类的，这对于保证 String 的不可变性是很重要的。

但这里有个注意点，假设我们给某个类加上了 final 关键字，这并不代表里面的成员变量自动被加上 final。事实上，这两者之 间不存在相互影响的关系，也就是说，类是 final 的，不代表里面的属性就会自动加上 final。
不过我们也记得，final 修饰方法的含义就是这个方法不允许被重写，而现在如果给这个类都加了 final，那这个类连子类都不 会有，就更不可能发生重写方法的情况。所以，其实在 final 的类里面，所有的方法，不论是 public、private 还是其他权限修 饰符修饰的，都会自动的、隐式的被指定为是 final 修饰的。