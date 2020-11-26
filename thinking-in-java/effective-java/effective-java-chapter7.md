---
title: 《Effective Java》读书笔记 第7章 方法
date: 2019-02-20 14:19:41
tags: ["Java", "读书笔记"]
toc: true
---

## 第38条：检查参数的有效性

对于公有的方法，要用Javadoc的`@throws`标签在文档中说明违反参数值会抛出的异常。一旦在文档中记录了对于方法参数的限制，并且记录了一旦违反这些限制将要抛出的异常，强加这些限制就是非常简单的事情了。

```java
 /**
     * Returns a {@code BigInteger} whose value is {@code this mod m}. The
     * modulus {@code m} must be positive. The result is guaranteed to be in the
     * interval {@code [0, m)} (0 inclusive, m exclusive). The behavior of this
     * function is not equivalent to the behavior of the % operator defined for
     * the built-in {@code int}'s.
     *
     * @param m the modulus.
     * @return {@code this mod m}.
     * @throws NullPointerException if {@code m == null}.
     * @throws ArithmeticException if {@code m < 0}.
     */
    public BigInteger mod(BigInteger m) {
        if (m.signum() <= 0) {
            throw new ArithmeticException("m.signum() <= 0");
        }
        return new BigInteger(BigInt.modulus(getBigInt(), m.getBigInt()));
    }
```

## 第39条：必要时进行保护性拷贝

## 第40条：谨慎设计方法签名

## 第41条：慎用重载

## 第42条：慎用可变参数

## 第43条：返回零长度的数组或者集合，而不是null

## 第44条：为所有到处的API元素编写文档注释