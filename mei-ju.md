# 枚举

## 1.定义一个枚举 <a id="1.&#x5B9A;&#x4E49;&#x4E00;&#x4E2A;&#x679A;&#x4E3E;"></a>

```java
public enum  WeekDay {

    SUN,MON,TUES,WED,THUR,FRI,SAT
}
```

枚举中的方法

```java
 WeekDay weekDay=WeekDay.FRI;
        System.out.println(weekDay);
        System.out.println(weekDay.name());
        System.out.println(weekDay.ordinal());//5
        System.out.println(WeekDay.valueOf("SUN").ordinal());//0
        //遍历
        for (WeekDay w:WeekDay.values()) {
            System.out.println(w);
        }
```

