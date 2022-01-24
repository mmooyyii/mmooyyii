代码展示了如何使用unix socket在进程间传递文件描述符, 从而实现TCP长连接服务的热更新.


### 演示流程

启动v1版本TCP服务器 `go run v1/v1.go`,使用telnet`telnet 127.0.0.1 18888`连接上去 输入任意字符后按回车,服务器会返回v1

```
moyi@DESKTOP-30UHID1:/mnt/c/Users/ADMIN/PycharmProjects/pythonProject/mmooyyii/codes/share_socket$ telnet 127.0.0.1 18888
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
123
v1
```

启动v2版本TCP服务器 `go run v2/v2.go`, 给v1服务器发一个sigint的信号(即ctrl+c), v1服务器退出, 再试试telnet的连接,发现tcp连接没有中断, 而且返回值变成了v2

```
moyi@DESKTOP-30UHID1:/mnt/c/Users/ADMIN/PycharmProjects/pythonProject/mmooyyii/codes/share_socket$ telnet 127.0.0.1 18888
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
123
v1
v2
v2
```