# 第2章 垃圾收集器与内存分配策略

## 2.1 概述

## 2.2 对象已死吗

```cpp
public class ReferenceCountingGC {
	public Object instance = null;
	private static final int _1MB = 1024 * 1024;
	private byte[] bigSize = new byte[2*_1MB];
	public static void main(String[] args){
		ReferenceCountingGC objA = new ReferenceCountingGC();
		ReferenceCountingGC objB = new ReferenceCountingGC();
		objA.instance = objB;
		objB.instance = objA;
		objA = null;
		objB = null;

		System.gc();	
	}
}
```