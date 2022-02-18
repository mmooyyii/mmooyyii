### 安全地关闭MPMC(multi-producer multi-consumer) channel


向一个已经关闭的channel中写数据会导致panic, 所以关闭channel前, 必须停止所有生产者.  
我们采用投票表决的方式(一定会同意),等全体同意后再关闭channel的方式关闭MPMC channel.
下面是示例代码


```go
package main

import (
	"fmt"
	"sync/atomic"
	"time"
)

var c chan int
var numberOfProducer = 5

var StopVote = int32(numberOfProducer)
var voteResult = make(chan int, 0)
var stop = make(chan int, 0)

func consumer(n int) {
	for range c {
	}
	fmt.Printf("消费者退出: %d\n", n)
}

func producer(n int) {
	for {
		select {
		case <-stop:
			if atomic.AddInt32(&StopVote, -1) == 0 {
				voteResult <- 1
			}
			fmt.Printf("生产者退出: %d\n", n)
			return
		case c <- 1:
			time.Sleep(time.Millisecond * 10)
		}
	}
}

func main() {
	c = make(chan int, 100)

	//启动消费者
	for i := 0; i < 5; i++ {
		go consumer(i)
	}
	//启动生产者
	for i := 0; i < numberOfProducer; i++ {
		go producer(i)
	}

	time.Sleep(time.Second)
	// 开始关闭
	// 通知生产者停止生产(发起退出投票)
	for i := 0; i < numberOfProducer; i++ {
		stop <- 1
	}
	<-voteResult // 等待投票结果,生产者全部退出
	// 关闭channel
	time.Sleep(time.Second)
	close(c)
	// 消费者退出

	time.Sleep(time.Second)
}


```
