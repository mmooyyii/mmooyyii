package main

import (
	"errors"
	"fmt"
	"sync/atomic"
)

type Consumer interface {
	Read([]byte)
}

type disruptor struct {
	ringbuffer    []byte
	readCursor    int64
	writeCursor   int64
	reserveCursor int64
	consumer      Consumer
}

func (d *disruptor) Put(text []byte) (err error) {
	if len(text) > len(d.ringbuffer) {
		return errors.New("text is too long")
	}
	l, r, err := d.Reserve(int64(len(text)))
	if err != nil {
		return err
	}
	if (l < d.readCursor && r > d.readCursor) || (l > d.readCursor && r > d.readCursor) {
		return errors.New("ringbuffer overflow")
	}
	if l > r {
		seg := len(d.ringbuffer) - int(l)
		copy(d.ringbuffer[l:], text[:seg])
		copy(d.ringbuffer[:r], text[seg:])
	} else {
		copy(d.ringbuffer[l:r], text)
	}
	d.Commit(r)
	return nil
}

func (d *disruptor) Reserve(n int64) (l, r int64, err error) {
	r = atomic.AddInt64(&d.reserveCursor, n)
	return r - n, r, nil
}

func (d *disruptor) Commit(n int64) {
	atomic.StoreInt64(&d.writeCursor, n)
}

func (d *disruptor) Read() {

}

func main() {
	d := &disruptor{
		ringbuffer:    make([]byte, 1<<4),
		readCursor:    0,
		writeCursor:   0,
		reserveCursor: 0,
	}
	err := d.Put([]byte("123123"))
	fmt.Println(err, d)
}
