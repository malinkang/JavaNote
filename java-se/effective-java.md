# 第1章 创建和销毁对象

## 第1条：考虑用静态工厂方法替代构造器

创建类实例最常用的方法就是提供一个公有的构造器。此外，还可以提供一个公有的`静态工厂方法（static factory method）`，它只是一个返回类的实例的静态方法。

```java
//来自Boolean的简单示例
//这个方法将boolean基本类型值转换成了一个Boolean对象引用：
public static Boolean valueOf(boolean b) {
    return b ? TRUE : FALSE;
}
```

**静态工厂方法与构造器不同的第一大优势在于，它们有名称。**

**静态工厂方法与构造器不同的第二大优势在于，不必在每次调用它们的时候都创建一个新对象。**这使得不可变类可以使用预先构建好的实例，或者将构件号的实例缓存起来，进行重复利用，从而避免创建不必要的重复对象。

**静态工厂方法与构造器不同的第三大优势在于，它们可以返回原返回类型的任何子类型的对象。**


**仅提供静态工厂方法的主要限制是没有公共或受保护构造函数的类不能被子类化。**

**静态工厂方法的第二个缺点是程序员很难找到它们。**在API文档中，它们没有像构造器那样在API文档中明确标识出来，因此，对于提供了静态工厂方法而不是构造器的类来说，要想查明如何实例化一个类，这是非常困难的。

静态工厂方法的一些惯用名称：

* from

```java
Date date = Date.from(instant);
```
* of

* valueOf

* instance或者getInstance

* create 或 newInstance

* getType

* newType

* type

## 第2条：遇到多个构造器参数时要考虑用构建器

静态工厂和构造器有个共同的局限性：它们都不能很好地扩展到大量的可选参数。考虑用一个类表示食品外面显示的营养成分标签。这些标签中有几个域是必需的：每份的含量、每罐的含量以及每份的卡路里，还有超过20个可选域：总脂肪量、饱和脂肪量、转化脂肪、胆固醇、钠等等。大多数产品在某几个可选域中都会有非零的值。

对于这样的类，程序员一向习惯采用**重叠构造器（telescoping constructor）**模式。

```java
public class NutritionFacts {
    private final int servingSize; //必选
    private final int servings; //必选
    private final int calories;//可选
    private final int fat; //可选
    private final int sodium; //可选
    private final int carbohydrate; //可选

    public NutritionFacts(int servingSize, int servings) {
        this(servingSize, servings, 0);
    }

    public NutritionFacts(int servingSize, int servings, int calories) {
        this(servingSize, servings, calories, 0);
    }

    public NutritionFacts(int servingSize, int servings, int calories, int fat) {
        this(servingSize, servings, calories, fat, 0);
    }

    public NutritionFacts(int servingSize, int servings, int calories, int fat, int sodium) {
        this(servingSize, servings, calories, fat, sodium, 0);
    }

    public NutritionFacts(int servingSize, int servings, int calories, int fat, int sodium, int carbohydrate) {
        this.servingSize = servingSize;
        this.servings = servings;
        this.calories = calories;
        this.fat = fat;
        this.sodium = sodium;
        this.carbohydrate = carbohydrate;
    }
}
```

**重叠构造器模式可行，但是当有许多参数的时候，客户端代码会很难编写，并且仍然较难以阅读**。

遇到许多构造器参数的时候，还有第二种替代方法，即`JavaBeans`模式。在这种模式下，调用一个无参构造器来创建对象，然后调用`setter`方法来设置每个必要的参数，以及每个相关的可选参数：

```java
public class NutritionFacts {
    private  int servingSize; //必选
    private  int servings; //必选
    private  int calories;//可选
    private  int fat; //可选
    private  int sodium; //可选
    private  int carbohydrate; //可选

    public void setServingSize(int servingSize) {
        this.servingSize = servingSize;
    }

    public void setServings(int servings) {
        this.servings = servings;
    }

    public void setCalories(int calories) {
        this.calories = calories;
    }

    public void setFat(int fat) {
        this.fat = fat;
    }

    public void setSodium(int sodium) {
        this.sodium = sodium;
    }

    public void setCarbohydrate(int carbohydrate) {
        this.carbohydrate = carbohydrate;
    }
}
```
```java
NutritionFacts cocaCola = new NutritionFacts();
cocaCola.setServingSize(240);
cocaCola.setServings(8);
cocaCola.setCalories(100);
cocaCola.setSodium(35);
cocaCola.setCarbohydrate(27);
```
遗憾的是，`JavaBeans`模式自身有着很严重的缺点。因为构造过程被分到了几个调用中，在构造过程中`JavaBean`可能处于不一致的状态。另一点不足在于，`JavaBeans`模式阻止了把类做成不可变的可能。

第三种替代方法`Builder`模式，既能保证像重叠构造器模式那样的安全性，也能保证像`JavaBeans`模式那么好的可读性。

```java
public class NutritionFacts {
    private final int servingSize; //必选
    private final int servings; //必选
    private final int calories;//可选
    private final int fat; //可选
    private final int sodium; //可选
    private final int carbohydrate; //可选

    public static class Builder {
        //必选参数
        private final int servingSize;
        private final int servings;
        //可选参数
        private int calories = 0;//可选
        private int fat = 0; //可选
        private int sodium = 0; //可选
        private int carbohydrate = 0; //可选

        public Builder(int servingSize, int servings) {
            this.servingSize = servingSize;
            this.servings = servings;
        }

        public Builder calories(int val) {
            calories = val;
            return this;
        }

        public Builder fat(int val) {
            fat = val;
            return this;
        }

        public Builder sodium(int val) {
            sodium = val;
            return this;
        }

        public Builder carbohydrate(int val) {
            carbohydrate = val;
            return this;
        }

        public NutritionFacts build() {
            return new NutritionFacts(this);
        }
    }

    private NutritionFacts(Builder builder) {
        servingSize = builder.servingSize;
        servings = builder.servings;
        calories = builder.calories;
        fat = builder.fat;
        sodium = builder.sodium;
        carbohydrate = builder.carbohydrate;
    }

}
```

调用

```java
 NutritionFacts cocaCola = new Builder(240, 8)
                .calories(100).sodium(35).carbohydrate(27).build();
```

`Builder`模式也有自身的不足。为了创建对象，必须先创建它的构造器。虽然创建构造器的开销在实践中可能不那么明显，但是在某些时分注重性能的情况下，可能就成问题了。`Builder`模式还比重叠构造器模式更加冗长，因此它只在有很多参数的时候才使用。

简而言之，如果类的构造器或者静态工厂具有多个参数，设计这种类时，`Builder`模式就是种不错的选择，特别是当大多数参数都是可选的时候。与使用传统的重叠构造器模式相比，使用`Builder`的客户端代码将更易于阅读和编写，构建起也比`JavaBeans`更加安全。