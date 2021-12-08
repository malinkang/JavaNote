# 取消与关闭

任务和线程的启动很容易，在大多数时候，我们都会让它们运行直到结束，或者让它们自行停止。然后，有时候我们希望提前结束任务或线程，或许是因为用户取消了操作，或者应用程序需要被快速关闭。

要使任务和线程能安全、快速、可靠地停止下来，并不是一件容易的事。Java没有提供任何机制来安全地终止线程。但它提供了中断（Interruption），这是一种协作机制，能够使一个线程终止另一个线程的当前工作。


## 任务取消

### 设置标志

在Java中没有一种安全的抢占式方法来停止线程，因此也就没有安全的抢占式方法来停止任务。只有一些**协作式**的机制，使请求取消的任务和代码都遵循一种协商好的协议。


其中一种协作机制能设置某个“已请求取消（Cancellation Requested）”标志，而任务将定期地查看该标志。如果设置了这个标志，那么任务将提前结束。

```java
public class PrimeGenerator implements Runnable {
    private final List<BigInteger> primes = new ArrayList<>();
    //必须设置为volatile
    private volatile boolean cancelled;

    @Override
    public void run() {
        BigInteger p = BigInteger.ONE;
        while (!cancelled) {
            p = p.nextProbablePrime();
            System.out.println("p = " + p);
            synchronized (this) {
                primes.add(p);
            }
        }
    }

    public void cancel() {
        cancelled = true;
    }

    public synchronized List<BigInteger> get() {
        return new ArrayList<>(primes);
    }

    static List<BigInteger> aSecondOfPrimes() throws InterruptedException {
        PrimeGenerator generator = new PrimeGenerator();
        new Thread(generator).start();
        try {
            TimeUnit.SECONDS.sleep(1);
        } finally {
            generator.cancel();
        }
        return generator.get();
    }

    public static void main(String[] args) throws InterruptedException {
        aSecondOfPrimes();
    }
}
```

### 中断


`PrimeGenerator`中的取消机制最终会使得搜索素数的任务退出，但在退出过程中需要花费一定的时间。然而，如果使用这种方法的任务调用了一个阻塞方法，例如`BlockingQueue.put`，那么可能会产生一个更严重的问题－任务可能永远不会检查取消标志，因此永远不会结束。

在下面的`BrokenPrimeProducer`就说明了这个问题。生产者线程生成素数，并将它们放入一个阻塞队列。如果生产者的速度超过了消费者的处理速度，队列将被填满，put方法也会阻塞。当生产者在put方法中阻塞时，如果消费者希望取消生产者任务，那么将发生什么情况？它可以调用cancel方法来设置 cancelled 标志，但此时生产者却永远不能检查这个标志，因为它无法从阻塞的put方法中恢复过来（因为消费者此时已经停止从队列中取出素数，所以put方法将一直保持阻塞状态）。

```java
package currency.cancel;

import java.math.BigInteger;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingDeque;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.TimeUnit;

public class BrokenPrimeProducer extends Thread{
    private final BlockingQueue<BigInteger> queue;
    private volatile boolean cancelled = false;
    BrokenPrimeProducer(BlockingQueue<BigInteger> queue){
        this.queue = queue;
    }

    @Override
    public void run() {
        try{
            BigInteger p = BigInteger.ONE;
            while (!cancelled){
                p = p.nextProbablePrime();
                System.out.println("producer "+p);
                queue.put(p);
            }
        }catch (InterruptedException consumed){

        }
    }
    public void cancel(){
        cancelled = true;
    }
    static void consumePrimes() throws InterruptedException {
        BlockingQueue<BigInteger> primes = new ArrayBlockingQueue<>(8);
        BrokenPrimeProducer producer = new BrokenPrimeProducer(primes);
        producer.start();
        try{
            TimeUnit.SECONDS.sleep(1);
            BigInteger p = primes.take();
            System.out.println("consumer "+p);
        }finally {
            producer.cancel();
        }
    }

    public static void main(String[] args) throws InterruptedException {
        consumePrimes();
    }
}

```

每个线程都有一个boolean类型的中断状态。当中断线程时，这个线程的中断状态将被设置为true。在Thread中包含了中断线程以及查线程中断状态的方法，如程序清单7-4所示。interrupt方法能中断目标线程，而isInterrupted方法能返回目标线程的中断状态。静态的interrupted方法将清除当前线程的中断状态，并返回它之前的值，这也是清除中断状态的唯一 方法。

阻塞库方法，例如Thread.sleep和 Object.wait等，都会检查线程何时中断，并且在发现中断提前返回。它们在响应中断时执行的操作包括：清除中断状态，抛出 InterruptedException；表示阻塞操作由于中断而提前结束。JVM并不能保证阻塞方法检测到中断的速度，但在实际情况中响应速度还是非常快的。

当线程在非阻塞状态下中断时，它的中断状态将被设置，然后根据将被取消的操作来检查中断状态以判断发生了中断。通过这样的方法，中断操作将变得“有黏性”－如果不触发InterruptedException，那么中断状态将一直保持，直到明确地清除中断状态。

对中断操作的正确理解是：它并不会真正地中断一个正在运行的线程，而只是发出中断请求，然后由线程在下一个合适的时刻中断自己。（这些时刻也被称为取消点）。有些方法，例如wait、sleep和join等，将严格地处理这种请求，当它们收到中断请求或者在开始执行时发现某个已被设置好的中断状态时，将抛出一个异常。设计良好的方法可以完全忽略这种请求，只要它们能使调用代码对中断请求进行某种处理。设计糟糕的方法可能会屏蔽中断请求，从而导致调用栈中的其他代码无法对中断请求作出响应。

在使用静态的interrupted时应该小心，因为它会清除当前线程的中断状态。如果在调用interrupted时返回了true，那么除非你想屏蔽这个中断，否则必须对它进行处理－可以抛出InterruptedException，或者通过再次调用 interrupt来恢复中断状态。BrokenPrimeProducer 说明了一些自定义的取消机制无法与可阻塞的库函数实现良好交互的原因。如果任务代码能够响应中断，那么可以使用中断作为取消机制，并且利用许多库类中提供的中断支持。

```java
public class PrimeProducer extends Thread{
    private final BlockingQueue<BigInteger> queue;
    PrimeProducer(BlockingQueue<BigInteger> queue){
        this.queue = queue;
    }

    @Override
    public void run() {
        try{
            BigInteger p = BigInteger.ONE;
            while(!Thread.currentThread().isInterrupted()){
                queue.put(p = p.nextProbablePrime());
            }
        }catch (InterruptedException consumed){
            
        }
    }
    public void cancel(){
        interrupt();
    }
}
```

### 响应中断

### 通过Future来实现取消

###  处理不可中断的阻塞

### 采用newTaskFor来封装非标准的取消


## 停止基于线程的服务


### 关闭ExecutorService

`ExecutorService`提供了两种关闭方法：使用`shutdown`正常关闭，以及使用`shutdownNow`强行关闭。在进行强行关闭时，`shutdownNow`首先关闭当前正在执行的任务，然后返回所有尚未启动的任务清单。

这两种关闭方式的差别在于各自的安全性和响应性：强制关闭的速度更快，但风险也更大，因为任务很可能在执行到一半时被结束：而正常关闭虽然速度慢，但却更安全，因为`ExecutorService`会一直等到队列中的所有任务都执行完成后才关闭。在其他拥有线程的服务中也应该考虑提供类似的关闭方式以供选择。

isShutdown()：它可以返回 true 或者 false 来判断线程池是否已经开始了关闭工作，也就是是否执行了 shutdown 或者 shutdownNow 方法。这里需要注意，如果调用 isShutdown() 方法的返回的结果为 true 并不代表线程池此时已经 彻底关闭了，这仅仅代表线程池开始了关闭的流程，也就是说，此时可能线程池中依然有线程在执行任务，队列里也可能有等 待被执行的任务。
isTerminated()：这个方法可以检测线程池是否真正“终结”了，这不仅代表线程池已关闭，同时代表线程池中 的所有任务都已经都执行完毕了，因为我们刚才说过，调用 shutdown 方法之后，线程池会继续执行里面未完成的任务，不仅 包括线程正在执行的任务，还包括正在任务队列中等待的任务。比如此时已经调用了 shutdown 方法，但是有一个线程依然在 执行任务，那么此时调用 isShutdown 方法返回的是 true ，而调用 isTerminated 方法返回的便是 false ，因为线程池中还有任务 正在在被执行，线程池并没有真正“终结”。直到所有任务都执行完毕了，调用 isTerminated() 方法才会返回 true，这表示线程 池已关闭并且线程池内部是空的，所有剩余的任务都执行完毕了。

awaitTermination()
第四个方法叫作 awaitTermination()，它本身并不是用来关闭线程池的，而是主要用来判断线程池状态的。比如我们给 awaitTermination 方法传入的参数是 10 秒，那么它就会陷入 10 秒钟的等待，直到发生以下三种情况之一:
1. 等待期间(包括进入等待状态之前)线程池已关闭并且所有已提交的任务(包括正在执行的和队列中等待的)都执行完 毕，相当于线程池已经“终结”了，方法便会返回 true;
2. 等待超时时间到后，第一种线程池“终结”的情况始终未发生，方法返回 false;
3. 等待期间线程被中断，方法会抛出 InterruptedException 异常。
也就是说，调用 awaitTermination 方法后当前线程会尝试等待一段指定的时间，如果在等待时间内，线程池已关闭并且内部的 任务都执行完毕了，也就是说线程池真正“终结”了，那么方法就返回 true，否则超时返回 fasle。


我们则可以根据 awaitTermination() 返回的布尔值来判断下一步应该执行的操作。


### shutdownNow的局限性

当通过 shutdownNow来强行关闭 ExecutorService时，它会尝试取消正在执行的任务，并返回所有已提交但尚未开始的任务，从而将这些任务写入日志或者保存起来以便之后进行处理。

然而，我们无法通过常规方法来找出哪些任务已经开始但尚未结束。这意味着我们无法在关闭过程中知道正在执行的任务的状态，除非任务本身会执行某种检查。要知道哪些任务还没有完成，你不仅需要知道哪些任务还没有开始，而且还需要知道当Executor关闭时哪些任务正在执行。 


## 处理非正常的线程终止


## JVM关闭

### 关闭钩子

### 守护线程

### 终结器

## 参考

* 《Java并发编程实战》第7章