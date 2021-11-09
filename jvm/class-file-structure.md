# 第6章 类文件结构

`Class`文件是一组以8位字节为基础单位的二进制流，各个数据项目严格按照顺序紧凑地排列在Class文件之中，中间没有添加任何分隔符，这使得整个Class文件中存储的内容几乎全部是程序运行的必要数据，没有空隙存在。当遇到需要占用8位字节以上空间的数据项时，则会按照高位在前的方式分割成若干个8位字节进行存储。




根据Java虚拟机规范的规定，Class文件格式采用一种类似于C语言结构体的伪结构来存储数据，这种伪结构中只有两种数据类型：无符号数和表：


* 无符号数属于基本的数据类型，以u1、u2、u4、u8来分别代表1个字节、2个字节、4个字节和8个字节的无符号数，无符号数可以用来描述数字、索引引用、数量值或者按照UTF-8编码构成字符串值。


* 表是由多个无符号数或者其他表作为数据项构成的复合数据类型，所有表都习惯性地以“_info”结尾。表用于描述有层次关系的复合结构的数据，整个Class文件本质上就是一张表。

![](https://malinkang-1253444926.cos.ap-beijing.myqcloud.com/images/jvm/c3aae0ad9dae466bbb09a756cc9f5876~tplv-k3u1fbpfcp-zoom-1.image)

编译下面代码输出Class文件：

```java
public class TestClass {
    private int m;
    public int inc(){
        return m + 1;
    }
}
```

vscode安装一个hexdump for VSCode插件，然后打开Class文件。

## 魔数

![](https://malinkang-1253444926.cos.ap-beijing.myqcloud.com/images/jvm/1d027160d7c743ef89da02a2b6adc10d~tplv-k3u1fbpfcp-zoom-1.image)

每个Class文件的头4个字节称为`魔数（Magic Number）`，它的唯一作用是确定这个文件是否为一个能被虚拟机接受的Class文件。很多文件存储标准中都使用魔数来进行身份识别，譬如图片格式，如gif或者jpeg等在文件头中都存有魔数。使用魔数而不是扩展名来进行识别主要是基于安全方面的考虑，因为文件扩展名可以随意地改动。文件格式的制定者可以自由地选择魔数值，只要这个魔数值还没有被广泛采用过同时又不会引起混淆即可。Class文件的魔数值为：`0xCAFEBABE`。

## 次版本号

![](https://malinkang-1253444926.cos.ap-beijing.myqcloud.com/images/jvm/eb5cd1bb02ef4a229422126816399394~tplv-k3u1fbpfcp-zoom-1.image)

代表次版本号的第5个和第6个字节值为`0x0000`。

## 主版本号

![](https://malinkang-1253444926.cos.ap-beijing.myqcloud.com/images/jvm/699f06cc9bba4a858275dfaf27fdb5bc~tplv-k3u1fbpfcp-zoom-1.image)

而主版本号的值为`0x0034`,也就是十进制的53。

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/8dbd6961ca0c4ecbbacb308cc9993818~tplv-k3u1fbpfcp-zoom-1.image)

## 常量池

紧接着主次版本号之后的是常量池入口，常量池可以理解为Class文件之中的资源仓库，它是Class文件结构中与其他项目关联最多的数据类型，也是占用Class文件空间最大的数据项目之一，同时它还是在Class文件中第一个出现的表类型数据项目。

### 常量池容量计数

由于常量池中常量的数量是不固定的，所以在常量池的入口需要放置一项u2类型的数据，代表常量池容量计数（constant_pool_count）。与Java中语言习惯不一样的是，这个容量计数是从1而不是0开始的。

![](https://malinkang-1253444926.cos.ap-beijing.myqcloud.com/images/jvm/68bb2269137d4868925852e22043f6c4~tplv-k3u1fbpfcp-zoom-1.image)

如上图所示，常量池容量为十六进制数0x0013，即十进制的19，这就代表常量池中有18项常量，索引值范围为1~18。在Class文件格式规范制定之时，设计者将第0项常量空出来是有特殊考虑的，这样做的目的在于满足后面某些指向常量池的索引值的数据在特定情况下需要表达“不引用任何一个常量池项目”的含义，这种情况就可以把索引值置为0来表示。Class文件结构中只有常量池的容量计数是从1开始，对于其他集合类型，包括接口索引集合、字段表集合、方法表集合等的容量计数都与一般习惯相同，是从0开始的。


常量池中主要存放两大类常量：字面量（Literal）和符号引用（Symbolic References）。字面量比较接近于Java语言层面的常量概念，如文本字符串、声明为final的常量值等。而符号引用则属于编译原理方面的概念，包括了下面几类常量：

* 被模块导出或者开放的包（Package）
* 类和接口的全限定名（Fully Qualified Name）
* 字段的名称和描述符（Descriptor）
* 方法的名称和描述符
* 方法句柄和方法类型（Method Handle、Method Type、Invoke Dynamic）
* 动态调用点和动态常量（Dynamically-Computed Call Site、Dynamically-Computed Constant）

Java代码在进行Javac编译的时候，并不像C和C++那样有“连接”这一步骤，而是在虚拟机加载Class文件的时候进行动态连接。也就是说，在Class文件中不会保存各个方法、字段的最终内存布局信息，因此这些字段、方法的符号引用不经过运行期转换的话无法得到真正的内存入口地址，也就无法直接被虚拟机使用。当虚拟机运行时，需要从常量池获得对应的符号引用，再在类创建时或运行时解析、翻译到具体的内存地址之中。

截至JDK 13，常量表中分别有17种不同类型的常量。这17类表都有一个共同的特点，表结构起始的第一位是个u1类型的标志位，代表着当前常量属于哪种常量类型。17种常量类型所代表的具体含义如表所示。

![](https://malinkang-1253444926.cos.ap-beijing.myqcloud.com/images/jvm/2d2ea14a984342e9af8a103230964dd8~tplv-k3u1fbpfcp-zoom-1.image)
![](https://malinkang-1253444926.cos.ap-beijing.myqcloud.com/images/jvm/92cd07347e524ac796f14d38046bddb7~tplv-k3u1fbpfcp-zoom-1.image)
![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/fc0be94e90ea4c5b8b8c6731148ef9b6~tplv-k3u1fbpfcp-zoom-1.image)

![](https://malinkang-1253444926.cos.ap-beijing.myqcloud.com/images/jvm/cc23765e40be40bf868b2134496bf972~tplv-k3u1fbpfcp-zoom-1.image)

常量池的第一项常量，标志位是`0A`，查表可知这个常量属于`CONSTANT_Methodref_info`类型。

![](https://malinkang-1253444926.cos.ap-beijing.myqcloud.com/images/jvm/3f61d67bb7c04910a448c6bec7d5d783~tplv-k3u1fbpfcp-zoom-1.image)
常量池的第二项常量，标志位是`09`，查表可知这个常量属于`CONSTANT_Fieldref_info`类型。

![](https://malinkang-1253444926.cos.ap-beijing.myqcloud.com/images/jvm/6cd7358c344f49deb2fd5a4779a614ae~tplv-k3u1fbpfcp-zoom-1.image)

第三项和第四项标识为都是`07`，属于`CONSTANT_Class_info`。

![](https://malinkang-1253444926.cos.ap-beijing.myqcloud.com/images/jvm/462c9f66d7aa4325989614b9b98bf642~tplv-k3u1fbpfcp-zoom-1.image)

第五项`CONSTANT_Utf8_info`。占用字节数为`1`,`6D`即十进制的109，对应ASCII值`m`。

* [ASCII对照表](https://tool.oschina.net/commons?type=4)

![](https://malinkang-1253444926.cos.ap-beijing.myqcloud.com/images/jvm/c6d7279733de48559e291b2c857ef2b6~tplv-k3u1fbpfcp-zoom-1.image)

第六项`CONSTANT_Utf8_info`。占用字节数为`1`,`6D`即十进制的73，对应ASCII值`I`。

![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/d7eaef7ccafd42669ddd3405af50a69f~tplv-k3u1fbpfcp-zoom-1.image)

第七项`CONSTANT_Utf8_info`。占用字节数为6。

![](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/1947115233bc49ab88411431300ed537~tplv-k3u1fbpfcp-zoom-1.image)
第八项`CONSTANT_Utf8_info`。占用字节数为3。

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/f887249fd02641d6b96ca1f68109a44d~tplv-k3u1fbpfcp-zoom-1.image)

第九项`CONSTANT_Utf8_info`。占用字节数为4。

![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/666d43acbae24f3da4bc371fe53f1def~tplv-k3u1fbpfcp-zoom-1.image)

第十项`CONSTANT_Utf8_info`。占用字节数为15。

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/ae8ec493d028443983748e0bd9b97a20~tplv-k3u1fbpfcp-zoom-1.image)

第十一项`CONSTANT_Utf8_info`。占用字节数为3。

![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/5276de0a0fc343bebe7bd292fbab1b6d~tplv-k3u1fbpfcp-zoom-1.image)

第十二项`CONSTANT_Utf8_info`。占用字节数为3。
![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/d6993bb3d0544929adce851356c870a2~tplv-k3u1fbpfcp-zoom-1.image)
第十三项`CONSTANT_Utf8_info`。占用字节数为10。

![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/6704d48e22df4d83aefbc3ed9f8224c6~tplv-k3u1fbpfcp-zoom-1.image)

第十四项`CONSTANT_Utf8_info`。占用字节数为14。

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/fc957302b15e465a81286f690153133f~tplv-k3u1fbpfcp-zoom-1.image)

第十五、十六项`CONSTANT_NameAndType_info`。

![](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/7ebcf44e5b3b4906b46b348b3ebe954b~tplv-k3u1fbpfcp-zoom-1.image)

第十七项`CONSTANT_Utf8_info`。占用字节数为9。

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/6a261fb44e7b4cbca71b0fa854b7d071~tplv-k3u1fbpfcp-zoom-1.image)
第十八项`CONSTANT_Utf8_info`。占用字节数为16。


在JDK的bin目录中，Oracle公司已经为我们准备好一个专门用于分析Class文件字节码的工具：javap。
![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/6fb2b990abff4e4ab3390ef7fcd7026a~tplv-k3u1fbpfcp-zoom-1.image)

## 访问标志

在常量池结束之后，紧接着的2个字节代表访问标志（access_flags），这个标志用于识别一些类或者接口层次的访问信息，包括：这个Class是类还是接口；是否定义为public类型；是否定义为abstract类型；如果是类的话，是否被声明为final；等等。具体的标志位以及标志的含义见表。
![](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/85201cce3e394d4e9c0fe889f73e943f~tplv-k3u1fbpfcp-zoom-1.image)

access_flags中一共有16个标志位可以使用，当前只定义了其中9个。没有使用到的标志位要求一律为零。TestClass是一个普通Java类，不是接口、枚举、注解或者模块，被public关键字修饰但没有被声明为final和abstract，并且它使用了JDK 1.2之后的编译器进行编译，因此它的ACC_PUBLIC、ACC_SUPER标志应当为真，而ACC_FINAL、ACC_INTERFACE、ACC_ABSTRACT、ACC_SYNTHETIC、ACC_ANNOTATION、ACC_ENUM、ACC_MODULE这七个标志应当为假。因此它的access_flags的值应为：0x0001|0x0020=0x0021。

![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/bf1addf75be04d4b8426b1758a585807~tplv-k3u1fbpfcp-zoom-1.image)

## 类索引、父类索引与接口索引集合

类索引（this_class）和父类索引（super_class）都是一个u2类型的数据，而接口索引集合（interfaces）是一组u2类型的数据的集合，Class文件中由这三项数据来确定该类型的继承关系。


类索引用于确定这个类的全限定名，父类索引用于确定这个类的父类的全限定名。由于Java语言不允许多重继承，所以父类索引只有一个，除了java.lang.Object之外，所有的Java类都有父类，因此除了java.lang.Object外，所有Java类的父类索引都不为0。

接口索引集合就用来描述这个类实现了哪些接口，这些被实现的接口将按implements关键字（如果这个Class文件表示的是一个接口，则应当是extends关键字）后的接口顺序从左到右排列在接口索引集合中。类索引、父类索引和接口索引集合都按顺序排列在访问标志之后，类索引和父类索引用两个u2类型的索引值表示，它们各自指向一个类型为CONSTANT_Class_info的类描述符常量，通过CONSTANT_Class_info类型的常量中的索引值可以找到定义在CONSTANT_Utf8_info类型的常量中的全限定名字符串。

![](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/718edb349a814a0d95e4fe6ec4377806~tplv-k3u1fbpfcp-zoom-1.image)

3个u2类型的值分别为0x0003、0x0004、0x0000，也就是类索引为3，父类索引为4，接口索引集合大小为0。
![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/7686c58cff0c4207a0951b97f450780d~tplv-k3u1fbpfcp-zoom-1.image)

## 字段表集合

字段表（field_info）用于描述接口或者类中声明的变量。Java语言中的“字段”（Field）包括类级变量以及实例级变量，但不包括在方法内部声明的局部变量。

字段可以包括的修饰符有
* 字段的作用域（public、private、protected修饰符）
* 是实例变量还是类变量（static修饰符）、可变性（final）、
* 并发可见性（volatile修饰符，是否强制从主内存读写）、
* 可否被序列化（transient修饰符）、
* 字段数据类型（基本类型、对象、数组）、
* 字段名称。

上述这些信息中，各个修饰符都是布尔值，要么有某个修饰符，要么没有，很适合使用标志位来表示。而字段叫做什么名字、字段被定义为什么数据类型，这些都是无法固定的，只能引用常量池中的常量来描述。

![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/a146dfe2780f49d8a193c0a3b42baaa4~tplv-k3u1fbpfcp-zoom-1.image)

字段修饰符放在access_flags项目中，它与类中的access_flags项目是非常类似的，都是一个u2的数据类型，其中可以设置的标志位和含义如表所示。
![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/65197eb9b8944bd2b1fdbb0e1f0a1fa3~tplv-k3u1fbpfcp-zoom-1.image)

很明显，由于语法规则的约束，ACC_PUBLIC、ACC_PRIVATE、ACC_PROTECTED三个标志最多只能选择其一，ACC_FINAL、ACC_VOLATILE不能同时选择。接口之中的字段必须有ACC_PUBLIC、ACC_STATIC、ACC_FINAL标志，这些都是由Java本身的语言规则所导致的。


跟随access_flags标志的是两项索引值：name_index和descriptor_index。它们都是对常量池项的引用，分别代表着字段的**简单名称**以及**字段和方法的描述符**。

全限定名和简单名称很好理解，“java/lang/String”是String类的全限定名，仅仅是把类全名中的“.”替换成了“/”而已，为了使连续的多个全限定名之间不产生混淆，在使用时最后一般会加入一个“；”号表示全限定名结束。简单名称则就是指没有类型和参数修饰的方法或者字段名称，`TestClass`类中的inc()方法和m字段的简单名称分别就是“inc”和“m”。

相比于全限定名和简单名称，方法和字段的描述符就要复杂一些。描述符的作用是用来描述字段的数据类型、方法的参数列表（包括数量、类型以及顺序）和返回值。根据描述符规则，基本数据类型（byte、char、double、float、int、long、short、boolean）以及代表无返回值的void类型都用一个大写字符来表示，而对象类型则用字符L加对象的全限定名来表示。

![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/9e6ce634d6fb47339ba2e97e859b861f~tplv-k3u1fbpfcp-zoom-1.image)

对于数组类型，每一维度将使用一个前置的“[”字符来描述，如一个定义为“java.lang.String[][]”类型的二维数组将被记录成“[[Ljava/lang/String；”，一个整型数组“int[]”将被记录成“[I”。

用描述符来描述方法时，按照先参数列表、后返回值的顺序描述，参数列表按照参数的严格顺序放在一组小括号“()”之内。如方法void inc()的描述符为“()V”，方法java.lang.String toString()的描述符为“()Ljava/lang/String；”，方法intindexOf(char[]source，int sourceOffset，int sourceCount，char[]target，inttargetOffset，int targetCount，int fromIndex)的描述符为“([CII[CIII)I”。

![](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/89a36861f4cd45e18d6bf24e18faa204~tplv-k3u1fbpfcp-zoom-1.image)

第一个u2类型的数据为容量计数器fields_count，其值为0x0001，说明这个类只有一个字段表数据。接下来紧跟着容量计数器的是access_flags标志，值为0x0002，代表private修饰符的ACC_PRIVATE标志位为真（ACC_PRIVATE标志的值为0x0002），其他修饰符为假。代表字段名称的name_index的值为0x0005，从代码清单6-2列出的常量表中可查得第五项常量是一个CONSTANT_Utf8_info类型的字符串，其值为“m”，代表字段描述符的descriptor_index的值为0x0006，指向常量池的字符串“I”。根据这些信息，我们可以推断出原代码定义的字段为“private int m；”。

在descrip-tor_index之后跟随着一个属性表集合，用于存储一些额外的信息，字段表可以在属性表中附加描述零至多项的额外信息。对于本例中的字段m，它的属性表计数器为0，也就是没有需要额外描述的信息，但是，如果将字段m的声明改为“final static int m=123；”，那就可能会存在一项名称为ConstantValue的属性，其值指向常量123。


字段表集合中不会列出从父类或者父接口中继承而来的字段，但有可能出现原本Java代码之中不存在的字段，譬如在内部类中为了保持对外部类的访问性，编译器就会自动添加指向外部类实例的字段。另外，在Java语言中字段是无法重载的，两个字段的数据类型、修饰符不管是否相同，都必须使用不一样的名称，但是对于Class文件格式来讲，只要两个字段的描述符不是完全相同，那字段重名就是合法的。

## 方法表集合

Class文件存储格式中对方法的描述与对字段的描述采用了几乎完全一致的方式，方法表的结构如同字段表一样，依次包括访问标志（access_flags）、名称索引（name_index）、描述符索引（descriptor_index）、属性表集合（attributes）几项，如表所示。这些数据项目的含义也与字段表中的非常类似，仅在访问标志和属性表集合的可选项中有所区别。

![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/a298ae1a3cf14b268a9829a948e328be~tplv-k3u1fbpfcp-zoom-1.image)

因为volatile关键字和transient关键字不能修饰方法，所以方法表的访问标志中没有了ACC_VOLATILE标志和ACC_TRANSIENT标志。与之相对，synchronized、native、strictfp和abstract关键字可以修饰方法，方法表的访问标志中也相应地增加了ACC_SYNCHRONIZED、ACC_NATIVE、ACC_STRICTFP和ACC_ABSTRACT标志。对于方法表，所有标志位及其取值可参见表：

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/64e9c5a44441425c934ee3af87dfb34c~tplv-k3u1fbpfcp-zoom-1.image)

方法的定义可以通过访问标志、名称索引、描述符索引来表达清楚，但方法里面的代码去哪里了？方法里的Java代码，经过Javac编译器编译成字节码指令之后，存放在方法属性表集合中一个名为“Code”的属性里面。

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/783e6ad69d884d3aa72469f182d8d417~tplv-k3u1fbpfcp-zoom-1.image)

第一个u2类型的数据（即计数器容量）的值为0x0002，代表集合中有两个方法，这两个方法为编译器添加的实例构造器`<init>`和源码中定义的方法inc()。第一个方法的访问标志值为0x0001，也就是只有ACC_PUBLIC标志为真，名称索引值为0x0007，常量池的方法名为`<init>`，描述符索引值为0x0008，对应常量为`()V`，属性表计数器attributes_count的值为0x0001，表示此方法的属性表集合有1项属性，属性名称的索引值为0x0009，对应常量为`Code`，说明此属性是方法的字节码描述。


## 属性表集合

Class文件、字段表、方法表都可以携带自己的属性表（attribute_info）集合，以描述某些场景专有的信息。

与Class文件中其他的数据项目要求严格的顺序、长度和内容不同，属性表集合的限制稍微宽松一些，不再要求各个属性表具有严格顺序，并且《Java虚拟机规范》允许只要不与已有属性名重复，任何人实现的编译器都可以向属性表中写入自己定义的属性信息，Java虚拟机运行时会忽略掉它不认识的属性。为了能正确解析Class文件，《Java虚拟机规范》最初只预定义了9项所有Java虚拟机实现都应当能识别的属性，而在最新的《Java虚拟机规范》的Java SE 12版本中，预定义属性已经增加到29项。

![](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/3b7cbe6f55df4b67af454f1b6777d733~tplv-k3u1fbpfcp-zoom-1.image)
![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/fe653d4a631d49fbbc3a1782faff629d~tplv-k3u1fbpfcp-zoom-1.image)

对于每一个属性，它的名称都要从常量池中引用一个CONSTANT_Utf8_info类型的常量来表示，而属性值的结构则是完全自定义的，只需要通过一个u4的长度属性去说明属性值所占用的位数即可。一个符合规则的属性表应该满足表中所定义的结构。

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/033808cd44d94ef4a76a835605d4dd3a~tplv-k3u1fbpfcp-zoom-1.image)

### 1.Code属性

Java程序方法体里面的代码经过Javac编译器处理之后，最终变为字节码指令存储在Code属性内。Code属性出现在方法表的属性集合之中，但并非所有的方法表都必须存在这个属性，譬如接口或者抽象类中的方法就不存在Code属性，如果方法表有Code属性存在，那么它的结构将如表所示。

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/04ca926c29e14327bd1f7229d8f232ca~tplv-k3u1fbpfcp-zoom-1.image)

attribute_name_index是一项指向CONSTANT_Utf8_info型常量的索引，此常量值固定为“Code”，它代表了该属性的属性名称，attribute_length指示了属性值的长度，由于属性名称索引与属性长度一共为6个字节，所以属性值的长度固定为整个属性表长度减去6个字节。

max_stack代表了操作数栈（Operand Stack）深度的最大值。在方法执行的任意时刻，操作数栈都不会超过这个深度。虚拟机运行的时候需要根据这个值来分配栈帧（Stack Frame）中的操作栈深度。

max_locals代表了局部变量表所需的存储空间。在这里，max_locals的单位是变量槽（Slot），变量槽是虚拟机为局部变量分配内存所使用的最小单位。对于byte、char、float、int、short、boolean和returnAddress等长度不超过32位的数据类型，每个局部变量占用一个变量槽，而double和long这两种64位的数据类型则需要两个变量槽来存放。方法参数（包括实例方法中的隐藏参数“this”）、显式异常处理程序的参数（Exception Handler Parameter，就是try-catch语句中catch块中所定义的异常）、方法体中定义的局部变量都需要依赖局部变量表来存放。注意，并不是在方法中用了多少个局部变量，就把这些局部变量所占变量槽数量之和作为max_locals的值，操作数栈和局部变量表直接决定一个该方法的栈帧所耗费的内存，不必要的操作数栈深度和变量槽数量会造成内存的浪费。Java虚拟机的做法是将局部变量表中的变量槽进行重用，当代码执行超出一个局部变量的作用域时，这个局部变量所占的变量槽可以被其他局部变量所使用，Javac编译器会根据变量的作用域来分配变量槽给各个变量使用，根据同时生存的最大局部变量数量和类型计算出max_locals的大小。

code_length和code用来存储Java源程序编译后生成的字节码指令。code_length代表字节码长度，code是用于存储字节码指令的一系列字节流。既然叫字节码指令，那顾名思义每个指令就是一个u1类型的单字节，当虚拟机读取到code中的一个字节码时，就可以对应找出这个字节码代表的是什么指令，并且可以知道这条指令后面是否需要跟随参数，以及后续的参数应当如何解析。我们知道一个u1数据类型的取值范围为0x00～0xFF，对应十进制的0～255，也就是一共可以表达256条指令。目前，《Java虚拟机规范》已经定义了其中约200条编码值对应的指令含义，编码与指令之间的对应关系可查阅本书的附录C“虚拟机字节码指令表”。

关于code_length，有一件值得注意的事情，虽然它是一个u4类型的长度值，理论上最大值可以达到2的32次幂，但是《Java虚拟机规范》中明确限制了一个方法不允许超过65535条字节码指令，即它实际只使用了u2的长度，如果超过这个限制，Javac编译器就会拒绝编译。一般来讲，编写Java代码时只要不是刻意去编写一个超级长的方法来为难编译器，是不太可能超过这个最大值的限制的。但是，某些特殊情况，例如在编译一个很复杂的JSP文件时，某些JSP编译器会把JSP内容和页面输出的信息归并于一个方法之中，就有可能因为方法生成字节码超长的原因而导致编译失败。

Code属性是Class文件中最重要的一个属性，如果把一个Java程序中的信息分为代码（Code，方法体里面的Java代码）和元数据（Metadata，包括类、字段、方法定义及其他信息）两部分，那么在整个Class文件里，Code属性用于描述代码，所有的其他数据项目都用于描述元数据。了解Code属性是学习后面两章关于字节码执行引擎内容的必要基础，能直接阅读字节码也是工作中分析Java代码语义问题的必要工具和基本技能，为此，笔者准备了一个比较详细的实例来讲解虚拟机是如何使用这个属性的。

![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/066059e0aa0e45a1ae712edc4a29e8a1~tplv-k3u1fbpfcp-zoom-1.image)


操作数栈的最大深度和本地变量表的容量都为0x0001，字节码区域所占空间的长度为0x0005。虚拟机读取到字节码区域的长度后，按照顺序依次读入紧随的5个字节，并根据字节码指令表翻译出所对应的字节码指令。翻译“2A B7000A B1”的过程为：

* 读入2A，查表得0x2A对应的指令为aload_0，这个指令的含义是将第0个变量槽中为reference类型的本地变量推送到操作数栈顶。
* 读入B7，查表得0xB7对应的指令为invokespecial，这条指令的作用是以栈顶的reference类型的数据所指向的对象作为方法接收者，调用此对象的实例构造器方法、private方法或者它的父类的方法。这个方法有一个u2类型的参数说明具体调用哪一个方法，它指向常量池中的一个CONSTANT_Methodref_info类型常量，即此方法的符号引用。
* 读入000A，这是invokespecial指令的参数，代表一个符号引用，查常量池得0x000A对应的常量为实例构造器“<init>()”方法的符号引用。
* 读入B1，查表得0xB1对应的指令为return，含义是从方法的返回，并且返回值为void。这条指令执行后，当前方法正常结束。
  
  

这段字节码虽然很短，但我们可以从中看出它执行过程中的数据交换、方法调用等操作都是基于栈（操作数栈）的。我们可以初步猜测，Java虚拟机执行字节码应该是基于栈的体系结构。但又发现与通常基于栈的指令集里都是无参数的又不太一样，某些指令（如invokespecial）后面还会带有参数。

我们再次使用javap命令把此Class文件中的另一个方法的字节码指令也计算出来

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/fab3ab77a72f4b0590bce556729bd910~tplv-k3u1fbpfcp-zoom-1.image)

如果大家注意到javap中输出的“Args_size”的值，可能还会有疑问：这个类有两个方法——实例构造器<init>()和inc()，这两个方法很明显都是没有参数的，为什么Args_size会为1？而且无论是在参数列表里还是方法体内，都没有定义任何局部变量，那Locals又为什么会等于1？如果有这样疑问的读者，大概是忽略了一条Java语言里面的潜规则：在任何实例方法里面，都可以通过“this”关键字访问到此方法所属的对象。这个访问机制对Java程序的编写很重要，而它的实现非常简单，仅仅是通过在Javac编译器编译的时候把对this关键字的访问转变为对一个普通方法参数的访问，然后在虚拟机调用实例方法时自动传入此参数而已。因此在实例方法的局部变量表中至少会存在一个指向当前对象实例的局部变量，局部变量表中也会预留出第一个变量槽位来存放对象实例的引用，所以实例方法参数值从1开始计算。这个处理只对实例方法有效，如果代码中的inc()方法被声明为static，那Args_size就不会等于1而是等于0了。

在字节码指令之后的是这个方法的显式异常处理表（下文简称“异常表”）集合，异常表对于Code属性来说并不是必须存在的，如代码清单6-4中就没有异常表生成。如果存在异常表，那它的格式应如表6-16所示，包含四个字段，这些字段的含义为：如果当字节码从第start_pc行到第end_pc行之间（不含第end_pc行）出现了类型为catch_type或者其子类的异常（catch_type为指向一个CONSTANT_Class_info型常量的索引），则转到第handler_pc行继续处理。当catch_type的值为0时，代表任意异常情况都需要转到handler_pc处进行处理。

  ![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/0a348e7b14424c6faf136eb0533ac302~tplv-k3u1fbpfcp-zoom-1.image)

异常表实际上是Java代码的一部分，尽管字节码中有最初为处理异常而设计的跳转指令，但《Java虚拟机规范》中明确要求Java语言的编译器应当选择使用异常表而不是通过跳转指令来实现Java异常及finally处理机制。

### 2.Exceptions属性

这里的Exceptions属性是在方法表中与Code属性平级的一项属性，读者不要与前面刚刚讲解完的异常表产生混淆。Exceptions属性的作用是列举出方法中可能抛出的受查异常（Checked Excepitons），也就是方法描述时在throws关键字后面列举的异常。

![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/684bd84cf1964450aea4e57b7a39a6a6~tplv-k3u1fbpfcp-zoom-1.image)

此属性中的number_of_exceptions项表示方法可能抛出number_of_exceptions种受查异常，每一种受查异常使用一个exception_index_table项表示；exception_index_table是一个指向常量池中CONSTANT_Class_info型常量的索引，代表了该受查异常的类型。

### 3.LineNumberTable属性

LineNumberTable属性用于描述Java源码行号与字节码行号（字节码的偏移量）之间的对应关系。它并不是运行时必需的属性，但默认会生成到Class文件之中，可以在Javac中使用-g：none或-g：lines选项来取消或要求生成这项信息。如果选择不生成LineNumberTable属性，对程序运行产生的最主要影响就是当抛出异常时，堆栈中将不会显示出错的行号，并且在调试程序的时候，也无法按照源码行来设置断点。LineNumberTable属性的结构如表所示。

![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/863c68b470fa4ab6b3b7dfa2eee1b33b~tplv-k3u1fbpfcp-zoom-1.image)

line_number_table是一个数量为line_number_table_length、类型为line_number_info的集合，line_number_info表包含start_pc和line_number两个u2类型的数据项，前者是字节码行号，后者是Java源码行号。


### 4.LocalVariableTable及LocalVariableTypeTable属性

  LocalVariableTable属性用于描述栈帧中局部变量表的变量与Java源码中定义的变量之间的关系，它也不是运行时必需的属性，但默认会生成到Class文件之中，可以在Javac中使用-g：none或-g：vars选项来取消或要求生成这项信息。如果没有生成这项属性，最大的影响就是当其他人引用这个方法时，所有的参数名称都将会丢失，譬如IDE将会使用诸如arg0、arg1之类的占位符代替原有的参数名，这对程序运行没有影响，但是会对代码编写带来较大不便，而且在调试期间无法根据参数名称从上下文中获得参数值。LocalVariableTable属性的结构如表所示。

  ![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/c8159e8a2a104633bed278f3f3e54d99~tplv-k3u1fbpfcp-zoom-1.image)

  其中local_variable_info项目代表了一个栈帧与源码中的局部变量的关联，结构如下表所示。

  ![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/7df1d915a3c740f582b08dd97a0d5946~tplv-k3u1fbpfcp-zoom-1.image)

start_pc和length属性分别代表了这个局部变量的生命周期开始的字节码偏移量及其作用范围覆盖的长度，两者结合起来就是这个局部变量在字节码之中的作用域范围。

name_index和descriptor_index都是指向常量池中CONSTANT_Utf8_info型常量的索引，分别代表了局部变量的名称以及这个局部变量的描述符。index是这个局部变量在栈帧的局部变量表中变量槽的位置。当这个变量数据类型是64位类型时（double和long），它占用的变量槽为index和index+1两个。


顺便提一下，在JDK 5引入泛型之后，LocalVariableTable属性增加了一个“姐妹属性”——LocalVariableTypeTable。这个新增的属性结构与LocalVariableTable非常相似，仅仅是把记录的字段描述符的descriptor_index替换成了字段的特征签名（Signature）。对于非泛型类型来说，描述符和特征签名能描述的信息是能吻合一致的，但是泛型引入之后，由于描述符中泛型的参数化类型被擦除掉，描述符就不能准确描述泛型类型了。因此出现了LocalVariableTypeTable属性，使用字段的特征签名来完成泛型的描述。


### 5.SourceFile及SourceDebugExtension属性

SourceFile属性用于记录生成这个Class文件的源码文件名称。这个属性也是可选的，可以使用Javac的-g：none或-g：source选项来关闭或要求生成这项信息。在Java中，对于大多数的类来说，类名和文件名是一致的，但是有一些特殊情况（如内部类）例外。如果不生成这项属性，当抛出异常时，堆栈中将不会显示出错代码所属的文件名。这个属性是一个定长的属性，其结构如表所示。
  ![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/131ea0d53ab84d3a8c2be25b84ec3e11~tplv-k3u1fbpfcp-zoom-1.image)

  sourcefile_index数据项是指向常量池中CONSTANT_Utf8_info型常量的索引，常量值是源码文件的文件名。为了方便在编译器和动态生成的Class中加入供程序员使用的自定义内容，在JDK5时，新增了SourceDebugExtension属性用于存储额外的代码调试信息。典型的场景是在进行JSP文件调试时，无法通过Java堆栈来定位到JSP文件的行号。JSR 45提案为这些非Java语言编写，却需要编译成字节码并运行在Java虚拟机中的程序提供了一个进行调试的标准机制，使用SourceDebugExtension属性就可以用于存储这个标准所新加入的调试信息，譬如让程序员能够快速从异常堆栈中定位出原始JSP中出现问题的行号。SourceDebugExtension属性的结构如表所示。

  ![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/ae47bc34fedf47258c13d8af35932259~tplv-k3u1fbpfcp-zoom-1.image)

  其中debug_extension存储的就是额外的调试信息，是一组通过变长UTF-8格式来表示的字符串。一个类中最多只允许存在一个SourceDebugExtension属性。


### 6.ConstantValue属性

  ConstantValue属性的作用是通知虚拟机自动为静态变量赋值。只有被static关键字修饰的变量（类变量）才可以使用这项属性。类似“int x=123”和“static intx=123”这样的变量定义在Java程序里面是非常常见的事情，但虚拟机对这两种变量赋值的方式和时刻都有所不同。对非static类型的变量（也就是实例变量）的赋值是在实例构造器`<init>()`方法中进行的；而对于类变量，则有两种方式可以选择：在类构造器`<clinit>()`方法中或者使用ConstantValue属性。目前Oracle公司实现的Javac编译器的选择是，如果同时使用final和static来修饰一个变量（按照习惯，这里称“常量”更贴切），并且这个变量的数据类型是基本类型或者java.lang.String的话，就将会生成ConstantValue属性来进行初始化；如果这个变量没有被final修饰，或者并非基本类型及字符串，则将会选择在`<clinit>()`方法中进行初始化。

  虽然有final关键字才更符合“ConstantValue”的语义，但《Java虚拟机规范》中并没有强制要求字段必须设置ACC_FINAL标志，只要求有ConstantValue属性的字段必须设置ACC_STATIC标志而已，对final关键字的要求是Javac编译器自己加入的限制。而对ConstantValue的属性值只能限于基本类型和String这点，其实并不能算是什么限制，这是理所当然的结果。因为此属性的属性值只是一个常量池的索引号，由于Class文件格式的常量类型中只有与基本属性和字符串相对应的字面量，所以就算ConstantValue属性想支持别的类型也无能为力。ConstantValue属性的结构如表所示。
![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/91a8752f901d47d8982f4170f2acd024~tplv-k3u1fbpfcp-zoom-1.image)

从数据结构中可以看出ConstantValue属性是一个定长属性，它的attribute_length数据项值必须固定为2。constantvalue_index数据项代表了常量池中一个字面量常量的引用，根据字段类型的不同，字面量可以是CONSTANT_Long_info、CONSTANT_Float_info、CONSTANT_Double_info、CONSTANT_Integer_info和CONSTANT_String_info常量中的一种。

### 7.InnerClasses属性

  InnerClasses属性用于记录内部类与宿主类之间的关联。如果一个类中定义了内部类，那编译器将会为它以及它所包含的内部类生成InnerClasses属性。InnerClasses属性的结构如表所示。



  ![](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/c4fa43b33cca4193b5bf6777126fc571~tplv-k3u1fbpfcp-zoom-1.image)
数据项number_of_classes代表需要记录多少个内部类信息，每一个内部类的信息都由一个inner_classes_info表进行描述。inner_classes_info表的结构如表6-25所示。

![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/b178de4b4a9c4e8a928dbcdafc5085cb~tplv-k3u1fbpfcp-zoom-1.image)  


  inner_class_info_index和outer_class_info_index都是指向常量池中CONSTANT_Class_info型常量的索引，分别代表了内部类和宿主类的符号引用。inner_name_index是指向常量池中CONSTANT_Utf8_info型常量的索引，代表这个内部类的名称，如果是匿名内部类，这项值为0。inner_class_access_flags是内部类的访问标志，类似于类的access_flags，它的取值范围如表所示。

  ![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/04bfa4f78686450aa343d05ab04040f6~tplv-k3u1fbpfcp-zoom-1.image)


 ### 8.Deprecated及Synthetic属性

  Deprecated和Synthetic两个属性都属于标志类型的布尔属性，只存在有和没有的区别，没有属性值的概念。Deprecated属性用于表示某个类、字段或者方法，已经被程序作者定为不再推荐使用，它可以通过代码中使用“@deprecated”注解进行设置。Synthetic属性代表此字段或者方法并不是由Java源码直接产生的，而是由编译器自行添加的，在JDK 5之后，标识一个类、字段或者方法是编译器自动产生的，也可以设置它们访问标志中的ACC_SYNTHETIC标志位。编译器通过生成一些在源代码中不存在的Synthetic方法、字段甚至是整个类的方式，实现了越权访问（越过private修饰器）或其他绕开了语言限制的功能，这可以算是一种早期优化的技巧，其中最典型的例子就是枚举类中自动生成的枚举元素数组和嵌套类的桥接方法（Bridge Method）。所有由不属于用户代码产生的类、方法及字段都应当至少设置Synthetic属性或者ACC_SYNTHETIC标志位中的一项，唯一的例外是实例构造器“<init>()”方法和类构造器“<clinit>()”方法。Deprecated和Synthetic属性的结构非常简单，如表所示。

![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/0c8fde3d818e4cea89c1f75a74240019~tplv-k3u1fbpfcp-zoom-1.image)

其中attribute_length数据项的值必须为0x00000000，因为没有任何属性值需要设置。


### 9.StackMapTable属性

  StackMapTable属性在JDK 6增加到Class文件规范之中，它是一个相当复杂的变长属性，位于Code属性的属性表中。这个属性会在虚拟机类加载的字节码验证阶段被新类型检查验证器（Type Checker）使用，目的在于代替以前比较消耗性能的基于数据流分析的类型推导验证器。

  这个类型检查验证器最初来源于Sheng Liang（听名字似乎是虚拟机团队中的华裔成员）实现为Java ME CLDC实现的字节码验证器。新的验证器在同样能保证Class文件合法性的前提下，省略了在运行期通过数据流分析去确认字节码的行为逻辑合法性的步骤，而在编译阶段将一系列的验证类型（Verification Type）直接记录在Class文件之中，通过检查这些验证类型代替了类型推导过程，从而大幅提升了字节码验证的性能。这个验证器在JDK 6中首次提供，并在JDK 7中强制代替原本基于类型推断的字节码验证器。关于这个验证器的工作原理，《Java虚拟机规范》在Java SE 7版中新增了整整120页的篇幅来讲解描述，其中使用了庞大而复杂的公式化语言去分析证明新验证方法的严谨性。


  StackMapTable属性中包含零至多个栈映射帧（Stack Map Frame），每个栈映射帧都显式或隐式地代表了一个字节码偏移量，用于表示执行到该字节码时局部变量表和操作数栈的验证类型。类型检查验证器会通过检查目标方法的局部变量和操作数栈所需要的类型来确定一段字节码指令是否符合逻辑约束。StackMapTable属性的结构如表所示。


  ![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/0b3f7db5aa4a4a7aba63f1483a0097e1~tplv-k3u1fbpfcp-zoom-1.image)

  在Java SE 7版之后的《Java虚拟机规范》中，明确规定对于版本号大于或等于50.0的Class文件，如果方法的Code属性中没有附带StackMapTable属性，那就意味着它带有一个隐式的StackMap属性，这个StackMap属性的作用等同于number_of_entries值为0的StackMapTable属性。一个方法的Code属性最多只能有一个StackMapTable属性，否则将抛出ClassFormatError异常。


### 10.Signature属性

  Signature属性在JDK 5增加到Class文件规范之中，它是一个可选的定长属性，可以出现于类、字段表和方法表结构的属性表中。在JDK 5里面大幅增强了Java语言的语法，在此之后，任何类、接口、初始化方法或成员的泛型签名如果包含了类型变量（Type Variable）或参数化类型（Parameterized Type），则Signature属性会为它记录泛型签名信息。之所以要专门使用这样一个属性去记录泛型类型，是因为Java语言的泛型采用的是擦除法实现的伪泛型，字节码（Code属性）中所有的泛型信息编译（类型变量、参数化类型）在编译之后都通通被擦除掉。使用擦除法的好处是实现简单（主要修改Javac编译器，虚拟机内部只做了很少的改动）、非常容易实现Backport，运行期也能够节省一些类型所占的内存空间。但坏处是运行期就无法像C#等有真泛型支持的语言那样，将泛型类型与用户定义的普通类型同等对待，例如运行期做反射时无法获得泛型信息。Signature属性就是为了弥补这个缺陷而增设的，现在Java的反射API能够获取的泛型类型，最终的数据来源也是这个属性。关于Java泛型、Signature属性和类型擦除，在第10章讲编译器优化的时候我们会通过一个更具体的例子来讲解。Signature属性的结构如表所示。

![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/04fc4a8e30aa41d69dbfa0b84de3dda3~tplv-k3u1fbpfcp-zoom-1.image)

  其中signature_index项的值必须是一个对常量池的有效索引。常量池在该索引处的项必须是CONSTANT_Utf8_info结构，表示类签名或方法类型签名或字段类型签名。如果当前的Signature属性是类文件的属性，则这个结构表示类签名，如果当前的Signature属性是方法表的属性，则这个结构表示方法类型签名，如果当前Signature属性是字段表的属性，则这个结构表示字段类型签名。


### 11．BootstrapMethods属性

  BootstrapMethods属性在JDK 7时增加到Class文件规范之中，它是一个复杂的变长属性，位于类文件的属性表中。这个属性用于保存invokedynamic指令引用的引导方法限定符。

  根据《Java虚拟机规范》（从Java SE 7版起）的规定，如果某个类文件结构的常量池中曾经出现过CONSTANT_InvokeDynamic_info类型的常量，那么这个类文件的属性表中必须存在一个明确的BootstrapMethods属性，另外，即使CONSTANT_InvokeDynamic_info类型的常量在常量池中出现过多次，类文件的属性表中最多也只能有一个BootstrapMethods属性。BootstrapMethods属性和JSR-292中的InvokeDynamic指令和java.lang.Invoke包关系非常密切，要介绍这个属性的作用，必须先讲清楚InovkeDynamic指令的运作原理。


  虽然JDK 7中已经提供了InovkeDynamic指令，但这个版本的Javac编译器还暂时无法支持InvokeDynamic指令和生成BootstrapMethods属性，必须通过一些非常规的手段才能使用它们。直到JDK 8中Lambda表达式和接口默认方法的出现，InvokeDynamic指令才算在Java语言生成的Class文件中有了用武之地。BootstrapMethods属性的结构如表所示。

![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/ea581d7fb1014593bbd6c188ddef0a94~tplv-k3u1fbpfcp-zoom-1.image)

  其中引用到的bootstrap_method结构如表所示。


  ![](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/caa11532f0fc4e60867ae442c869ebd7~tplv-k3u1fbpfcp-zoom-1.image)

  BootstrapMethods属性里，num_bootstrap_methods项的值给出了bootstrap_methods[]数组中的引导方法限定符的数量。而bootstrap_methods[]数组的每个成员包含了一个指向常量池CONSTANT_MethodHandle结构的索引值，它代表了一个引导方法。还包含了这个引导方法静态参数的序列（可能为空）。bootstrap_methods[]数组的每个成员必须包含以下三项内容：

  * bootstrap_method_ref：bootstrap_method_ref项的值必须是一个对常量池的有效索引。常量池在该索引处的值必须是一个CONSTANT_MethodHandle_info结构。
  * num_bootstrap_arguments：num_bootstrap_arguments项的值给出了bootstrap_argu-ments[]数组成员的数量。
  * bootstrap_arguments[]：bootstrap_arguments[]数组的每个成员必须是一个对常量池的有效索引。常量池在该索引出必须是下列结构之一：CONSTANT_String_info、CONSTANT_Class_info、CONSTANT_Integer_info、CONSTANT_Long_info、CONSTANT_Float_info、CONSTANT_Double_info、CONSTANT_MethodHandle_info或CONSTANT_MethodType_info。

### 12．MethodParameters属性


  MethodParameters是在JDK 8时新加入到Class文件格式中的，它是一个用在方法表中的变长属性。MethodParameters的作用是记录方法的各个形参名称和信息。


  最初，基于存储空间的考虑，Class文件默认是不储存方法参数名称的，因为给参数起什么名字对计算机执行程序来说是没有任何区别的，所以只要在源码中妥当命名就可以了。随着Java的流行，这点确实为程序的传播和二次复用带来了诸多不便，由于Class文件中没有参数的名称，如果只有单独的程序包而不附加上JavaDoc的话，在IDE中编辑使用包里面的方法时是无法获得方法调用的智能提示的，这就阻碍了JAR包的传播。后来，“-g：var”就成为了Javac以及许多IDE编译Class时采用的默认值，这样会将方法参数的名称生成到LocalVariableTable属性之中。不过此时问题仍然没有全部解决，LocalVariableTable属性是Code属性的子属性——没有方法体存在，自然就不会有局部变量表，但是对于其他情况，譬如抽象方法和接口方法，是理所当然地可以不存在方法体的，对于方法签名来说，还是没有找到一个统一完整的保留方法参数名称的地方。所以JDK 8中新增的这个属性，使得编译器可以（编译时加上-parameters参数）将方法名称也写进Class文件中，而且MethodParameters是方法表的属性，与Code属性平级的，可以运行时通过反射API获取。MethodParameters的结构如表所示。
  ![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/d63ff0b320df4cadb98d42e4265783a7~tplv-k3u1fbpfcp-zoom-1.image)
  其中，引用到的parameter结构如表所示。
  ![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/1b3a00b2083b4d20ae78d17b07b83bf0~tplv-k3u1fbpfcp-zoom-1.image)

  其中，name_index是一个指向常量池CONSTANT_Utf8_info常量的索引值，代表了该参数的名称。而access_flags是参数的状态指示器，它可以包含以下三种状态中的一种或多种：
  * 0x0010（ACC_FINAL）：表示该参数被final修饰。
  * 0x1000（ACC_SYNTHETIC）：表示该参数并未出现在源文件中，是编译器自动生成的。
  * 0x8000（ACC_MANDATED）：表示该参数是在源文件中隐式定义的。Java语言中的典型场景是this关键字。

### 13．模块化相关属性

  JDK 9的一个重量级功能是Java的模块化功能，因为模块描述文件（module-info.java）最终是要编译成一个独立的Class文件来存储的，所以，Class文件格式也扩展了Module、ModulePackages和ModuleMainClass三个属性用于支持Java模块化相关功能。Module属性是一个非常复杂的变长属性，除了表示该模块的名称、版本、标志信息以外，还存储了这个模块requires、exports、opens、uses和provides定义的全部内容，其结构如表所示。


  ![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/ab4a0361b9ce413f91bae25fe91314a0~tplv-k3u1fbpfcp-zoom-1.image)

  其中，module_name_index是一个指向常量池CONSTANT_Utf8_info常量的索引值，代表了该模块的名称。而module_flags是模块的状态指示器，它可以包含以下三种状态中的一种或多种：·0x0020（ACC_OPEN）：表示该模块是开放的。·0x1000（ACC_SYNTHETIC）：表示该模块并未出现在源文件中，是编译器自动生成的。·0x8000（ACC_MANDATED）：表示该模块是在源文件中隐式定义的。module_version_index是一个指向常量池CONSTANT_Utf8_info常量的索引值，代表了该模块的版本号。后续的几个属性分别记录了模块的requires、exports、opens、uses和provides定义，由于它们的结构是基本相似的，为了节省版面，笔者仅介绍其中的exports，该属性结构如表所示。

![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/bf618ec864df443599ec687ad12ebeaa~tplv-k3u1fbpfcp-zoom-1.image)


  exports属性的每一元素都代表一个被模块所导出的包，exports_index是一个指向常量池CONSTANT_Package_info常量的索引值，代表了被该模块导出的包。exports_flags是该导出包的状态指示器，它可以包含以下两种状态中的一种或多种：

  * 0x1000（ACC_SYNTHETIC）：表示该导出包并未出现在源文件中，是编译器自动生成的。
  * 0x8000（ACC_MANDATED）：表示该导出包是在源文件中隐式定义的。


  exports_to_count是该导出包的限定计数器，如果这个计数器为零，这说明该导出包是无限定的（Unqualified），即完全开放的，任何其他模块都可以访问该包中所有内容。如果该计数器不为零，则后面的exports_to_index是以计数器值为长度的数组，每个数组元素都是一个指向常量池中CONSTANT_Module_info常量的索引值，代表着只有在这个数组范围内的模块才被允许访问该导出包的内容。

  ModulePackages是另一个用于支持Java模块化的变长属性，它用于描述该模块中所有的包，不论是不是被export或者open的。该属性的结构如表所示。

![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/08bb4e5fcec54b408fb90b6b0c317edf~tplv-k3u1fbpfcp-zoom-1.image)


package_count是package_index数组的计数器，package_index中每个元素都是指向常量池CONSTANT_Package_info常量的索引值，代表了当前模块中的一个包。最后一个ModuleMainClass属性是一个定长属性，用于确定该模块的主类（MainClass），其结构如表所示。



  ![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/538c8206a810449094bff0d9f43ba1d1~tplv-k3u1fbpfcp-zoom-1.image)

  其中，main_class_index是一个指向常量池CONSTANT_Class_info常量的索引值，代表了该模块的主类。


  ### 14．运行时注解相关属性

 早在JDK 5时期，Java语言的语法进行了多项增强，其中之一是提供了对注解（Annotation）的支持。为了存储源码中注解信息，Class文件同步增加了RuntimeVisibleAnnotations、RuntimeInvisibleAnnotations、RuntimeVisibleParameterAnnotations和RuntimeInvisibleParameter-Annotations四个属性。到了JDK 8时期，进一步加强了Java语言的注解使用范围，又新增类型注解（JSR 308），所以Class文件中也同步增加了RuntimeVisibleTypeAnnotations和RuntimeInvisibleTypeAnnotations两个属性。由于这六个属性不论结构还是功能都比较雷同，因此我们把它们合并到一起，以RuntimeVisibleAnnotations为代表进行介绍。

  RuntimeVisibleAnnotations是一个变长属性，它记录了类、字段或方法的声明上记录运行时可见注解，当我们使用反射API来获取类、字段或方法上的注解时，返回值就是通过这个属性来取到的。RuntimeVisibleAnnotations属性的结构如表所示。

  ![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/a93cf21b2b104035b2b0dcfde81b7315~tplv-k3u1fbpfcp-zoom-1.image)
  num_annotations是annotations数组的计数器，annotations中每个元素都代表了一个运行时可见的注解，注解在Class文件中以annotation结构来存储，具体如表所示。

  ![](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/8e6f66b33e664b5389092078dfd16539~tplv-k3u1fbpfcp-zoom-1.image)

  type_index是一个指向常量池CONSTANT_Utf8_info常量的索引值，该常量应以字段描述符的形式表示一个注解。num_element_value_pairs是element_value_pairs数组的计数器，element_value_pairs中每个元素都是一个键值对，代表该注解的参数和值。
