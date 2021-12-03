# 字符串

## 使用正则表达式

在jdk 1.4的版本中，java添加了支持正则表达式的包`java.util.regex`。

Pattern对象常用方法

* compile\(\)
* split\(\)
* matches\(\)

```java
  // 获取正则表达式 输出 \d+
        System.out.println(p.pattern());
        String[] strs = p.split("kkkk2hhhh3nnnn4mmmm5");
        for (int i=0;i<strs.length;i++){
            System.out.println(strs[i]);
        }
//        kkkk
//        hhhh
//        nnnn
//
        System.out.println(Pattern.matches("\\d+","22222"));
        // true

        Matcher matcher=p.matcher("2333ss22");

        System.out.println(matcher.matches());
        // false
        System.out.println(matcher.lookingAt());
        // true 前面有匹配的

        System.out.println(matcher.find());
        // true
        // 匹配的字符可以在任意位置

       System.out.println(matcher.start());
        // 6

        System.out.println(matcher.end());
```





## 参考

* [正则表达式30分钟入门教程](http://deerchao.net/tutorials/regex/regex.htm)

