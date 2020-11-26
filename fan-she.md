# 反射

通过反射API可以获取程序在运行时刻的内部结构。知道Java类的内部结构之后，就可以与它进行交互，包括创建新的对象和调用对象中的方法等。这种交互方式与直接在源代码中使用效果是相同的。

## 1.获取Class对象 <a id="1.&#x83B7;&#x53D6;Class&#x5BF9;&#x8C61;"></a>

Class是一个java类，跟Java API中定义的诸如Thread、Integer类、我们自己定义的类是一样，也继承了Object（Class是Object的直接子类）。总之，必须明确一点，它其实只是个类，只不过名字比较特殊。

于我们自己定义的类，我们用类来抽象现实中的某些事物，比如我们定义一个名称为Car的类来抽象现实生活中的车，然后可以实例化这个类，用这些实例来表示我的车、你的车、黄的车、红的车等等。 好了，现在回到Class 类上来，这个类它抽象什么了？它的实例又表示什么呢？ 在一个运行的程序中，会有许多类和接口存在。我们就用Class这个类来表示对这些类和接口的抽象，而Class类的每个实例则代表运行中的一个类。例如，运行的程序有A、B、C三个类，那么Class类就是对A、B、C三个类的抽象。所谓抽象，就是提取这些类的一些共同特征，比如说这些类都有类名，都有对应的hashcode，可以判断类型属于class、interface、enum还是annotation。这些可以封装成Class类的域，另外可以定义一些方法，比如获取某个方法、获取类型名等等。这样就封装了一个表示类型\(type\)的类。

需要注意的是，这个特殊的Class类没有公开的构造函数，那怎么获取Class类的实例呢？有几个途径。

1. 当Java虚拟机载入一个类的时候，它就会自动创建一个Class类的实例来表示这个类。例如，虚拟机载入Car这个来的时候，它就会创建一个Class类的实例。然后可以通过以下方法获得这个Class对象：

   ```java
   Class clazz = Car.class;
   ```

2. 可以通过调用类的getClass\(\)方法来获取Class类的实例

   ```java
   Car car = new Car();
   Class clazz = car.class;
   ```

3. 通过调用Class的forName方法获取Class类的实例

```text
Class clazz = Class.forName("java.lang.String");
```

## Method

* getDeclaringClass 获取声明此方法的类

```java
     //boolean addAll(Collection<? extends E> c);
      Method method =  List.class.getMethod("addAll", Collection.class);
        // 获取参数
       Parameter[] parameters= method.getParameters();
        for(int i=0;i<parameters.length;i++){
            System.out.println(parameters[i]);
            //java.util.Collection<? extends E> arg0
        }
        Type[] types1=method.getGenericParameterTypes();

        for(int i=0;i<types1.length;i++){
            System.out.println(types1[i]);
            // 输出 java.util.Collection<? extends E>

            if(types1[i] instanceof ParameterizedType){
                Type type=((ParameterizedType)types1[i]).getRawType();
                System.out.println("rawtype-->"+type);
                // 输出 rawtype-->interface java.util.Collection
            }
        }

       Type[] types2 = method.getParameterTypes();

        for(int i=0;i<types2.length;i++){
            System.out.println(types2[i]);


            // 输出 interface java.util.Collection
        }


        Method method2 =  List.class.getMethod("iterator");
        Type type1= method2.getReturnType();

        System.out.println(type1);
        // 输出 interface java.util.Iterator

        Type type2= method2.getGenericReturnType();

        System.out.println(type2);

        //java.util.Iterator<E>
```

