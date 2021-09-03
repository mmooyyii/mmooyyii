package main

import (
	"net"
	"os"
	"reflect"
	"syscall"
)

type TcpServer struct {
	listen net.Listener
	conn   []net.Conn
	master net.Conn
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
			return
		}
		t.conn = append(t.conn, conn)
		if t.master == nil {
			t.master = conn
			go func() {
				file := os.NewFile(ConnToFd(conn), "")
				for _, c := range t.conn {
					file.Seek(0, 0)
					_, _ = syscall.Sendfile(int(ConnToFd(c)), int(file.Fd()), nil, 4<<20)
				}
				conn.Close()
			}()
		}
	}
}

func ConnToFd(c net.Conn) uintptr {
	fd := reflect.ValueOf(c).
		Elem().
		FieldByName("conn").
		FieldByName("fd").
		Elem().
		FieldByName("pfd").
		FieldByName("Sysfd").
		Int()
	return uintptr(fd)
}

func main() {
	t := &TcpServer{}
	t.startLoop("127.0.0.1:18888")
}
