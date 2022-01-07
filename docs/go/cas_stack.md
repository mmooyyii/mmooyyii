# 用cas实现的无锁栈

在main里简单的测了一下正常运行, 不知道有没有其他问题.

```go
package main

import (
	"fmt"
	"sync"
	"sync/atomic"
	"unsafe"
)

type CasStack struct {
	Top  unsafe.Pointer
	size int64
}

func NewCasStack() *CasStack {
	return &CasStack{Top: nil}
}

type Node struct {
	val  interface{}
	next unsafe.Pointer
}

func NewNode(value interface{}) *Node {
	return &Node{val: value, next: nil}
}

func (stack *CasStack) Push(value interface{}) {
	for {
		node := NewNode(value)
		oldValue := stack.Top
		node.next = oldValue
		newValue := unsafe.Pointer(node)
		if atomic.CompareAndSwapPointer(&stack.Top, oldValue, newValue) {
			atomic.AddInt64(&stack.size, 1)
			return
		}
	}
}

func (stack *CasStack) Pop() interface{} {
	if stack.Top == nil {
		panic("pop a empty stack")
	}
	for {
		oldValue := stack.Top
		newValue := (*Node)(stack.Top).next
		if atomic.CompareAndSwapPointer(&stack.Top, oldValue, newValue) {
			atomic.AddInt64(&stack.size, -1)
			return (*Node)(oldValue).val
		}
	}
}

func main() {
	stack := NewCasStack()
	wg := sync.WaitGroup{}
	for i := 0; i < 100; i++ {
		wg.Add(1)
		go func() {
			for i := 0; i < 100; i++ {
				stack.Push(i)
				stack.Pop()
			}
			wg.Done()
		}()
	}
	wg.Wait()
	fmt.Println(stack.size)
	fmt.Println(stack)
}

```

