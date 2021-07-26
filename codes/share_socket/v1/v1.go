package main

import (
	"fmt"
	"net"
	"os"
	"os/signal"
	"share_socket"
	"syscall"
)

var unixSocket = "/tmp/unix"

type TcpServer struct {
	listen net.Listener
	conn   []net.Conn
}

func (t *TcpServer) Update() {
	fmt.Println("start update")
	raddr, _ := net.ResolveUnixAddr("unix", unixSocket)
	unixConn, _ := net.DialUnix("unix", nil, raddr)
	share_socket.SendListener(unixConn, t.listen)
	for _, c := range t.conn {
		share_socket.SendSocket(unixConn, c)
	}
}

func (t *TcpServer) startLoop(address string) {
	listener, err := net.Listen("tcp", address)
	if err != nil {
		panic(err.Error())
	}
	t.listen = listener
	for {
		conn, err := listener.Accept()
		if err != nil {
			return // 终止程序
		}
		t.conn = append(t.conn, conn)
		go handle(conn)
	}
}

func handle(conn net.Conn) {
	for {
		buf := make([]byte, 512)
		_, err := conn.Read(buf)
		if err != nil {
			fmt.Println("Error reading", err.Error())
			return
		}
		_, err = conn.Write([]byte("v1"))
		if err != nil {
			return
		}
	}
}

func main() {
	t := &TcpServer{}
	go t.startLoop("127.0.0.1:18888")
	signals := make(chan os.Signal, 1)
	signal.Notify(signals, syscall.SIGINT)
	<-signals
	t.Update()
	fmt.Scanln()
}
