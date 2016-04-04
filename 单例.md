## 枚举


<h3 id="1.定义一个枚举">1.定义一个枚举<h3>

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

