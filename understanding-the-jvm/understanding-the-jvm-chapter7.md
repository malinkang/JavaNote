# 第7章 虚拟机类加载机制

## 7.1 概述

## 7.2 类加载的时机

从被加载到虚拟机内存中开始，到卸载出内存为止，它的整个生命周期包括：加载（Loading）、验证（Verification）、准备（Preparation）、解析（Resolution）、初始化（Initialization）、使用（Using）和卸载（Unloading）7个阶段。其中验证、准备、解析3个部分统称为连接（Linking），这7个阶段的发生顺序如图7-1所示。

![&#x56FE;7-1&#x7C7B;&#x7684;&#x751F;&#x547D;&#x5468;&#x671F;](https://github.com/malinkang/JavaNote/tree/05f7c6abd740c7af6029fb75682bad60b7d55521/images/understanding-the-jvm/7-1.png)

## 7.3 类加载的过程

### 7.3.1 加载

### 7.3.2 验证

验证是连接阶段的第一步，这一阶段的目的是为了确保Class文件的字节流中包含的信息符合当前虚拟机的要求，并且不会危害虚拟机自身的安全。

#### 1.文件格式验证

#### 2.元数据验证

#### 3.字节码验证

#### 4.符号引用验证

### 7.3.3 准备

### 7.3.4 解析

#### 1.类或接口的解析

#### 2.字段解析

#### 3.类方法解析

#### 4.接口方法解析

### 7.3.5 初始化

## 7.4 类加载器

虚拟机设计团队把类加载阶段中的“通过一个类的全限定名来获取描述此类的二进制字节流”这个动作放到Java虚拟机外部去实现，以便让应用程序自己决定如何去获取所需要的类。实现这个动作的代码模块称为“类加载器”。

### 7.4.1 类与类加载器

### 7.4.2 双亲委派模型

Java虚拟机的角度来讲，只存在两种不同的类加载器：一种是启动类加载器（Bootstrap ClassLoader），这个类加载器使用C++语言实现￼，是虚拟机自身的一部分；另一种就是所有其他的类加载器，这些类加载器都由Java语言实现，独立于虚拟机外部，并且全都继承自抽象类java.lang.ClassLoader。

从Java开发人员的角度来看，类加载器还可以划分得更细致一些，绝大部分Java程序都会使用到以下3种系统提供的类加载器。

* 启动类加载器（Bootstrap ClassLoader）：前面已经介绍过，这个类将器负责将存放在`<JAVA_HOME>\lib`目录中的，或者被-Xbootclasspath参数所指定的路径中的，并且是虚拟机识别的（仅按照文件名识别，如rt.jar，名字不符合的类库即使放在lib目录中也不会被加载）类库加载到虚拟机内存中。启动类加载器无法被Java程序直接引用，用户在编写自定义类加载器时，如果需要把加载请求委派给引导类加载器，那直接使用null代替即可，如代码清单7-9所示为java.lang.ClassLoader.getClassLoader\(\)方法的代码片段。
* 扩展类加载器（Extension ClassLoader）：这个加载器由sun.misc.Launcher$ExtClassLoader实现，它负责加载\lib\ext目录中的，或者被java.ext.dirs系统变量所指定的路径中的所有类库，开发者可以直接使用扩展类加载器。
* 应用程序类加载器（Application ClassLoader）：这个类加载器由sun.misc.Launcher$App-ClassLoader实现。由于这个类加载器是ClassLoader中的getSystemClassLoader\(\)方法的返回值，所以一般也称它为系统类加载器。它负责加载用户类路径（ClassPath）上所指定的类库，开发者可以直接使用这个类加载器，如果应用程序中没有自定义过自己的类加载器，一般情况下这个就是程序中默认的类加载器。

我们的应用程序都是由这3种类加载器互相配合进行加载的，如果有必要，还可以加入自己定义的类加载器。这些类加载器之间的关系一般如图7-2所示。

![&#x56FE;7-2&#x7C7B;&#x52A0;&#x8F7D;&#x5668;&#x53CC;&#x4EB2;&#x59D4;&#x6D3E;&#x6A21;&#x578B;](https://github.com/malinkang/JavaNote/tree/05f7c6abd740c7af6029fb75682bad60b7d55521/images/understanding-the-jvm/7-2.png)

### 7.4.3 破坏双亲委派模型

