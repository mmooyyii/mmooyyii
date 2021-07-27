package share_socket

import (
	"errors"
	"fmt"
	"net"
	"os"
	"reflect"
	"syscall"
)

func SendListener(unixConn *net.UnixConn, l net.Listener) {
	fmt.Println("send listener")
	fd := ListenerToFd(l)
	oob := syscall.UnixRights(int(fd))
	_, _, _ = unixConn.WriteMsgUnix([]byte("lister"), oob, nil)
}

func SendSocket(unixConn *net.UnixConn, conn net.Conn) {
	fmt.Println("send conn")
	fd := ConnToFd(conn)
	oob := syscall.UnixRights(int(fd))
	_, _, _ = unixConn.WriteMsgUnix([]byte("client"), oob, nil)
}

func ReceiveFd(conn *net.UnixConn) (string, uintptr, error) {
	buf := make([]byte, 32)
	oob := make([]byte, 32)
	bufn, oobn, _, _, _ := conn.ReadMsgUnix(buf, oob)
	buf = buf[:bufn]
	scms, _ := syscall.ParseSocketControlMessage(oob[:oobn])
	if len(scms) == 0 {
		return "", 0, errors.New("unix domain close")
	}
	fds, _ := syscall.ParseUnixRights(&(scms[0]))
	return string(buf), uintptr(fds[0]), nil
}

func ListenerToFd(c net.Listener) uintptr {
	fd := reflect.ValueOf(c).Elem().
		FieldByName("fd").
		Elem().
		FieldByName("pfd").
		FieldByName("Sysfd").
		Int()
	return uintptr(fd)
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

func FdToConn(fd uintptr) net.Conn {
	file := os.NewFile(fd, "")
	socket, _ := net.FileConn(file)
	return socket
}

func FdToListener(fd uintptr) net.Listener {
	file := os.NewFile(fd, "")
	listener, _ := net.FileListener(file)
	return listener
}
