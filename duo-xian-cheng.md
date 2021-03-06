# 多线程

## 目录

## 1.创建线程

在Java中，有两种方式创建线程：

1.通过直接继承Thread类，然后覆盖run\(\)方法。

```java
  private static class CalculatorTask extends Thread{
        @Override
        public void run() {
            System.out.println("子线程开始计算...");
            int sum=0;
            for (int i = 0; i < 1000; i++) {
                sum+=i;
            }
            System.out.println("计算结果："+sum);

        }
    }
```

2.实现Runnable接口，然后传递给Thread类作为构造参数。

```java
   private static class CalculatorTask implements Runnable{
        @Override
        public void run() {
            System.out.println("子线程开始计算...");
            int sum=0;
            for (int i = 0; i < 1000; i++) {
                sum+=i;
            }
            System.out.println("计算结果："+sum);

        }
    }

  new Thread(new CalculatorTask()).start();
```

## Callable、Future和FutureTask <a id="Callable&#x3001;Future&#x548C;FutureTask"></a>

创建线程有两种方式：1.直接继承Thread。2.实现Runnable接口。这两种方式都有一个明显的缺陷就是：在执行完任务之后无法获取执行结果。

Java 1.5提供了`Callable`和`Future`，通过它们可以在任务执行完毕之后得到任务执行结果。

### Callable

`Callable`是一个接口，里面只声明了一个方法`call()`。

```java
public interface Callable<V> {
    /**
     * Computes a result, or throws an exception if unable to do so.
     *
     * @return computed result
     * @throws Exception if unable to compute a result
     */
    V call() throws Exception;
}
```

`Callable`一般情况下是配合`ExecutorService`来使用，在`ExecutorService`接口中声明了若干个`submit`方法的重载。

```java
    <T> Future<T> submit(Callable<T> task);
    <T> Future<T> submit(Runnable task, T result);
    Future<?> submit(Runnable task);
```

### Future

`Future`就是对具体的`Runnable`或者`Callable`任务的执行结果进行取消，查询是否完成，还可以通过get方法获取执行结果。

```java
public interface Future<V> {
    boolean cancel(boolean mayInterruptIfRunning);
    boolean isCancelled();
    boolean isDone();
    V get() throws InterruptedException, ExecutionException;
    V get(long timeout, TimeUnit unit)
        throws InterruptedException, ExecutionException, TimeoutException;
}
```

`Future`中声明了5个方法：

* cancel方法用来取消任务，如果取消任务成功则返回true，如果取消任务失败则返回false。参数mayInterruptIfRunning表示是否允许取消正在执行却没有执行完毕的任务，如果设置true，则表示可以取消正在执行过程中的任务。如果任务已经完成，则无论mayInterruptIfRunning为true还是false，此方法肯定返回false，即如果取消已经完成的任务会返回false；如果任务正在执行，若mayInterruptIfRunning设置为true，则返回true，若mayInterruptIfRunning设置为false，则返回false；如果任务还没有执行，则无论mayInterruptIfRunning为true还是false，肯定返回true。
* isCancelled方法表示任务是否被取消成功，如果在任务正常完成前被取消成功，则返回 true。
* isDone方法表示任务是否已经完成，若任务完成，则返回true；
* get\(\)方法用来获取执行结果，这个方法会产生阻塞，会一直等到任务执行完毕才返回；
* get\(long timeout, TimeUnit unit\)用来获取执行结果，如果在指定时间内，还没获取到结果，就直接返回null。

下面用例子来演示使用`Callable`和`Future`来获取执行结果。

```java
 public static void main(String[] args) {

        ExecutorService executor= Executors.newCachedThreadPool();
        Task task=new Task();

        Future<?> result=executor.submit(futureTask);

        System.out.println("主线程在执行任务...");
        try {
            System.out.println("task运行结果"+result.get());
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }
        System.out.println("执行完毕...");
    }


class Task implements Callable<Integer>{

    @Override
    public Integer call() throws Exception {
        System.out.println("子线程在进行计算...");
        int sum=0;
        for (int i = 0; i < 1000; i++) {
            sum+=i;
        }
        return sum;
    }
}
```

执行结果

```text
主线程在执行任务...
子线程在进行计算...
task运行结果499500
执行完毕...
```

### FutureTask

```java
public class FutureTask<V> implements RunnableFuture<V>

public interface RunnableFuture<V> extends Runnable, Future<V>
```

通过查看源码，可以知道`FutureTask`实现了`Future`和`Runnable`接口。所以它既可以作为`Runnable`被线程执行，又可以作为`Future`得到`Callable`的返回值。

`FutureTask`提供了两个构造函数

```java
public FutureTask(Callable<V> callable) {
}
public FutureTask(Runnable runnable, V result) {
}
```

使用`Callable`和`FutureTask`来获取执行结果。

```java
public static void main(String[] args) {
        ExecutorService executor= Executors.newCachedThreadPool();
        Task task=new Task();
        FutureTask<Integer> futureTask=new FutureTask<Integer>(task);
        executor.submit(futureTask);

        System.out.println("主线程在执行任务...");
        try {
            System.out.println("task运行结果"+result.get());
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }
        System.out.println("执行完毕...");
    }
```

执行结果

```text
主线程在执行任务...
子线程在进行计算...
task运行结果499500
执行完毕...
```

