# 注解

## 1.注解定义

使用@interface自定义注解时，自动继承了java.lang.annotation.Annotation接口，由编译程序自动完成其他细节。在定义注解时，不能继承其他的注解或接口。@interface用来声明一个注解，其中的每一个方法实际上是声明了一个配置参数。方法的名称就是参数的名称，返回值类型就是参数的类型。可以通过default来声明参数的默认值。

注解参数的可支持数据类型：

1. 所有基本数据类型
2. String类型
3. Class类型
4. enum类型
5. Annotation类型
6. 以上所有类型的数组

Annotation类型参数只能用public或者默认这两个访问权限。

如果参数名设置成value，则使用时不必指定参数名。

## 2.元注解

元注解的作用就是负责注解其他注解。Java5.0定义了4个原注解，它们被用来提供对其它 annotation类型作说明。Java5.0定义的元注解： 1. @Target 2. @Retention 3. @Documented 4. @Inherited

2.1@Target @Target用于描述注解的使用范围。 取值范围

```java
public enum ElementType {
    /** Class, interface (including annotation type), or enum declaration */
    TYPE,

    /** Field declaration (includes enum constants) */
    FIELD,

    /** Method declaration */
    METHOD,

    /** Formal parameter declaration */
    PARAMETER,

    /** Constructor declaration */
    CONSTRUCTOR,

    /** Local variable declaration */
    LOCAL_VARIABLE,

    /** Annotation type declaration */
    ANNOTATION_TYPE,

    /** Package declaration */
    PACKAGE,

    /**
     * Type parameter declaration
     *
     * @since 1.8
     */
    TYPE_PARAMETER,

    /**
     * Use of a type
     *
     * @since 1.8
     */
    TYPE_USE
}
```

2.2@Retention @Retention表示需要在什么级别保存该注释信息，用于描述注解的生命周期。

取值范围

```java
public enum RetentionPolicy {
    /**
     * Annotations are to be discarded by the compiler.
     */
    SOURCE,

    /**
     * Annotations are to be recorded in the class file by the compiler
     * but need not be retained by the VM at run time.  This is the default
     * behavior.
     */
    CLASS,

    /**
     * Annotations are to be recorded in the class file by the compiler and
     * retained by the VM at run time, so they may be read reflectively.
     *
     * @see java.lang.reflect.AnnotatedElement
     */
    RUNTIME
}
```

## 3.提取注解

方法

* getAnnotation
* getAnnotations：
* getDeclaredAnnotations
* isAnnotationPresent:判断该程序元素上是否包含指定类型的注解，存在返回true，不存在返回false

注解的方法

* annotationType

