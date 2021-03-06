# 基础

## 1.开发环境搭建 <a id="1.&#x5F00;&#x53D1;&#x73AF;&#x5883;&#x642D;&#x5EFA;"></a>

略

## 2.Java编译与运行 <a id="2.Java&#x7F16;&#x8BD1;&#x4E0E;&#x8FD0;&#x884C;"></a>

使用记事本编写如下代码，并保存为HelloWorld.java

```java
package com.malinkang;
public class HelloWorld {
    public static void main(String[] args){
        System.out.println("Hello,World");
    }
}
```

在命令行下执行如下命令进行编译。

```text
javac -d ./Dropbox/Code/JavaDemo/com/malinkang ./Dropbox/Code/JavaDemo/HelloWorld.java
```

`-d`指定编译后的.class文件存放的目录

编译成功之后，运行程序

```text
java -cp ./Dropbox/Code/JavaDemo com.malinkang.HelloWorld
```

`-cp`用于指定环境变量。

## 3.进制 <a id="3.&#x8FDB;&#x5236;"></a>

二进制转换十进制

1001 1×2 + 0×2+ 0×2+ 1×2 ＝9

二进制转换为八进制

101001 -&gt; 101 001 -&gt;51

[十进制转换二进制](http://www.wikihow.com/Convert-from-Decimal-to-Binary)

## 4.源码补码反码 <a id="4.&#x6E90;&#x7801;&#x8865;&#x7801;&#x53CD;&#x7801;"></a>

1.原码

将最高位作为符号位（以0代表正，1代表负），其余各位代表数值本身的绝对值（以二进制表示）。 为了简单起见，我们用1个字节来表示一个整数。

```text
 +7的原码为： 00000111
 -7的原码为： 10000111
```

2.反码

一个数如果为正，则它的反码与原码相同；一个数如果为负，则符号位为1，其余各位是对原码取反。 为了简单起见，我们用1个字节来表示一个整数：

```text
     +7的反码为：00000111
     -7的反码为： 11111000
```

3.补码

补码：一个数如果为正，则它的原码、反码、补码相同；一个数如果为负，则符号位为1，其余各位是对原码取反，然后整个数加1。为了简单起见，我们用1个字节来表示一个整数：

```text
+7的补码为： 00000111
-7的补码为： 11111001
```

已知一个负数的补码，将其转换为十进制数，步骤：

* 1、先对各位取反；
* 2、将其转换为十进制数；
* 3、加上负号，再减去1。

```text
11111010，最高位为1，是负数，先对各位取反得00000101，转换为十进制数得5，加上负号得-5，再减1得-6
```

## 5.数据类型 <a id="5.&#x6570;&#x636E;&#x7C7B;&#x578B;"></a>

## 6.类型提升和强制转换 <a id="6.&#x7C7B;&#x578B;&#x63D0;&#x5347;&#x548C;&#x5F3A;&#x5236;&#x8F6C;&#x6362;"></a>

## 7.运算符 <a id="7.&#x8FD0;&#x7B97;&#x7B26;"></a>

## 参考

* [补码之美](https://github.com/lifesinger/lifesinger.github.com/issues/187)

