# 面向对象

## 构造函数 <a id="&#x6784;&#x9020;&#x51FD;&#x6570;"></a>

构造函数用于在调用对象之前进行初始化工作。构造函数名称必须与类名完全相同。没有任何参数的构造器称为**默认构造器**。如果在类中没有写构造器，则编译器会自动帮你创建一个默认构造器。如果定义了一个构造器，编译器就不会帮你自动创建默认构造器。

在Java中，初始化和创建捆绑在一起，两者不能分离。

new表达式返回了新建对象的引用，构造函数没有返回值，这与返回值为`void`明显不同。

## 重载 <a id="&#x91CD;&#x8F7D;"></a>

被重载的方法必须改变参数列表，甚至参数顺序不同也足以区分两个方法。不过一般情况下别这么做，因为这会使代码难以维护。

```java
public class Person {
    private String name;
    private int age;

    public Person(String name,int age){
        this.name=name;
        this.age=age;
    }
    public Person(int age,String name){
        this.age=age;
        this.name=name;
    }
}
```

用时可能并不关心方法的返回值，像`f();`这样根本无法知道函数的返回值类型，如果返回值可以通过返回值来区分，则无法知道调用的是那个f\(\)。所以不能通过返回值来区分重载。

* 被重载的方法可以改变访问修饰符
* 被重载的方法可以声明新的或更广的检查异常；
* 方法能够在同一个类中或者在一个子类中被重载

## this关键字

使用this只能调用一个构造器，必须将构造器调用置于最起始处，否则编译器会报错。

```java
public class Person {
    private String name;
    private int age;

    public Person(String name,int age){
        this.name=name;
        this.age=age;
    }
    public Person(int age,String name){
       this(name,age);
    }
}
```

## 成员初始化 <a id="&#x6210;&#x5458;&#x521D;&#x59CB;&#x5316;"></a>

Java中所有的变量必须初始化。对于局部变量如果不初始化将编译不通过。全局变量是基本数据类型如果不初始化都有一个默认的初始值，如果是对象引用，不尽兴初始化，引用就会获得一个特殊的值`null`。

## 构造器初始化 <a id="&#x6784;&#x9020;&#x5668;&#x521D;&#x59CB;&#x5316;"></a>

变量定义的先后顺序决定了初始化的顺序，直接赋值，会在任何方法\(包括构造函数\)被调用之前得到初始化。

```java
public class Window {
    Window(int marker){
        System.out.println("Window( "+marker+" )");
    }
}
public class House {
    Window w1 = new Window(1);

    House(){
        System.out.println("House()");
        w3 = new Window(33);
    }
    Window w2 = new Window(2);

    void f(){
        System.out.println("f()");
    }

    Window w3 = new Window(3);
}
House house =new House();

house.f();
```

输出

```text
Window( 1 )
Window( 2 )
Window( 3 )
House()
Window( 33 )
f()
```

## 静态数据初始化 <a id="&#x9759;&#x6001;&#x6570;&#x636E;&#x521D;&#x59CB;&#x5316;"></a>

当第一次创建对象，或者第一次访问静态数据的时候，静态变量才会初始化。

```java
public class Bowl {

    Bowl(int marker){
        System.out.println("Bowl(" + marker + ")");
    }

    public void f1(int marker){
        System.out.println("f1(" + marker +")");
    }
}
public class Cupboard {
     Bowl bowl3 = new Bowl(3);

    static Bowl bowl4 = new Bowl(4);

    Cupboard(){
        System.out.println("Cupboard()");
        bowl4.f1(1);
    }

    public void f3(int marker){
        System.out.println("f1(" + marker +")");
    }


    static Bowl bowl5 = new Bowl(5);
}

public class Table {

    static Bowl bowl1 = new Bowl(1);

    Table(){
        System.out.println("Table()");
        bowl2.f1(1);
    }

    public void f2(int marker){
        System.out.println("f1(" + marker +")");
    }

    static Bowl bowl2 = new Bowl(2);
}

    public static void main(String[] args) {

        System.out.println("Creating new Cupboard() in main");
        new Cupboard();
        System.out.println("Creating new Cupboard() in main");
        new Cupboard();
        table.f2(1);
         cupboard.f3(1);
    }
```

输出

```text
Bowl(1)
Bowl(2)
Table()
f1(1)
Bowl(4)
Bowl(5)
Bowl(3)
Cupboard()
f1(1)
Creating new Cupboard() in main
Bowl(3)
Cupboard()
f1(1)
Creating new Cupboard() in main
Bowl(3)
Cupboard()
f1(1)
f1(1)
f1(1)
```

对象创建过程

1. 虽然没有static关键字，构造器也是静态方法。因此，当首次创建对象时，或者类的静态方法静态域首次被访问时，Java解释器必须查找类路径，以定位.class文件。
2. 载入Class对象，有关静态初始化的所有动作都会执行。因此静态初始化只在Class对象首次加载的时候进行一次。
3. 当用new创建对象时，首先将在堆上为对象分配足够的存储空间
4. 存储空间会被清零，自动为对象的基本数据都设置成默认值，而引用则被设置成null。
5. 执行所有字段定义出的初始化。
6. 执行构造器。

## 重写 <a id="&#x91CD;&#x5199;"></a>

* 参数列表必须完全与被重写方法的相同；
* 返回类型必须完全与被重写方法的返回类型相同；
* 访问级别的限制性一定不能比被重写方法的强；
* 重写方法一定不能抛出新的检查异常或比被重写的方法声明的检查异常更广泛的检查异常。
* 非私有非静态方法不能被任何静态方法覆写，如果子类中试着以静态方式（不管访问权限修饰符是什么）来覆写父类的方法，编译时会报错。
* 非私有静态方法不能被任何非静态方法覆写，如果子类中试着以非静态方式（不管访问权限修饰符是什么）来覆写父类的方法，编译时会报错。

```java
public class A {
    public void overwrite(int i) throws IOException {}
}

class B extends A {
    // !! 编译通不过，不能缩小访问权限
    //    void overwrite(int i) throws IOException {}

    // !! 编译通不过，不能扩大异常范围
    //    public void overwrite(int i) throws Exception {}

    // 正常，编译没问题，可以不抛出异常
    // public void overwrite(int i) {}

    // 覆写父类方法
    public void overwrite(int i) throws IOException {}

    protected void overload(int i) {}

    //重载上面的方法
    int overload(long i) throws IOException {
        return 0;
    }
}
```

```java
public class A {
    public int i = 10;
}
public class B extends A{
    public int i = 20;
}
public static void main(String[] args) {
        B b = new B();
        A a = b;

        System.out.println(b.i);// 20
        System.out.println(a.i);// 10
    }
```

```java
public class A {
    public int i = 10;

    public void printI(){
        System.out.println(i);
    }
}
public class B extends A{
    public int i = 20;
}
public static void main(String[] args) {
        B b = new B();
        A a = b;

        b.printI();//10
        a.printI();//10
    }
```

```java
public class A {
    public int i = 10;

    public void printI(){
        System.out.println(i);
    }
}
public class B extends A{
    public int i = 20;
    public void printI(){
        System.out.println(i);
    }
}
public static void main(String[] args) {
        B b = new B();
        A a = b;

        b.printI();//20
        a.printI();//20
    }
```

* [Java构造时成员初始化的陷阱](http://coolshell.cn/articles/1106.html)

