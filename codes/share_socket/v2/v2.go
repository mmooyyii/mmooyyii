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

func (t *TcpServer) startLoop() {
	_ = syscall.Unlink(unixSocket)
	laddr, _ := net.ResolveUnixAddr("unix", unixSocket)
	listener, _ := net.ListenUnix("unix", laddr)
	conn, _ := listener.AcceptUnix()
	for {
		tp, fd := share_socket.ReceiveFd(conn)
		if tp == "lister" {
			l := share_socket.FdToListener(fd)
			t.listen = l
			go func() {
				for {
					conn, err := l.Accept()
					if err != nil {
						return
					}
					t.conn = append(t.conn, conn)
					go handle(conn)
				}
			}()
		} else {
			conn := share_socket.FdToConn(fd)
			t.conn = append(t.conn, conn)
			go handle(conn)
		}
	}
}

func handle(conn net.Conn) {
	fmt.Println("new Conn")
	for {
		buf := make([]byte, 512)
		_, err := conn.Read(buf)
		if err != nil {
			fmt.Println("Error reading", err.Error())
			return
		}
		_, err = conn.Write([]byte("v2"))
		if err != nil {
			return
		}
	}
}

func main() {
	t := &TcpServer{}
	go t.startLoop()
	signals := make(chan os.Signal, 1)
	signal.Notify(signals, syscall.SIGINT)
	<-signals
}
