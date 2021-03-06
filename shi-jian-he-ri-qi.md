# 时间和日期

## 1.Date类

### 1.1构造函数

* public Date\(\)：创建一个当前时间的Date对象。
* public Date\(long date\)：传入一个距离1970年1月1日起的毫秒数。

### 1.2常用方法

* public long getTime\(\)：返回自1970年1月1日00:00:00 以来的毫秒数。
* public void setTime\(long time\)：
* public boolean after\(Date when\)：若当调用此方法的Date对象在指定日期之后返回true,否则返回false。
* boolean before\(Date date\)：若当调用此方法的Date对象在指定日期之前返回true,否则返回false。

### 1.3字符串格式化

```java
        Date date = new Date();
        SimpleDateFormat sdf=new SimpleDateFormat("yyyy年MM月dd日");
        System.out.println(sdf.format(date));
        //2015年06月24日
```

SimpleDateFormat还可以将字符串转换为Date对象。

```java
        SimpleDateFormat sdf=new SimpleDateFormat("yyyy年MM月dd日");
        System.out.println(sdf.parse("2000年1月1日"));
        //Sat Jan 01 00:00:00 CST 2000
```

时间模式字符串

| 模式字母 | 描述 |
| :--- | :--- |
| **y** | 年 |
| M | 一年中的月份 |
| w | 一年中的星期 |
| W | 月份中的星期 |
| d | 月份中的日 |
| D | 一年中的日 |
| H | 一天中的小时-介于0到23之间的数字 |
| k | 一天中的小时-介于1到24之间的数字 |
| K | 上午或下午中的小时-介于0到11之间的数字 |
| h | 上午或下午中的小时-介于1到12之间的数字 |
| m | 小时中的分钟 |
| s | 分钟中的秒钟 |
| S | 毫秒 |

## 2.Calendar类

### 2.1常用方法

* public static Calendar getInstance\(\)：返回一个表示当前时间的calendar的对象。
* public void set\(int field, int value\)
* public int get\(int field\)
* public void add\(int field, int amount\)
* public final Date getTime\(\)
* public final void setTime\(Date date\)
* public long getTimeInMillis\(\)

