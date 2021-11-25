### 对以长连接tcp为主的服务器进行热更新  


一般的热更新会使用关闭一台机器  
在某一服务器上有较多的tcp长连接，要热更新该服务器的代码，一个问题就是如何保持这些连接不断的情况下更新  

对与一个tcp连接,会在服务器与客户端都存在一个socket用于2者直接的消息交互  
而socket的本质是一个 int ` int socket(int, int, int); sys/socket.h`   
对于操作系统来说socket是一个文件描述符   

所以只要新建一个新代码的进程，然后将客户端socket交给新进程，socket交付完成后，关闭旧进程，  
在新进程中绑定原先的端口，继续accept新的连接，即完成热更新   
示例代码
[server](https://github.com/mmooyyii/mmooyyii/blob/master/code/hot_update_server.py)  
[client](https://github.com/mmooyyii/mmooyyii/blob/master/code/hot_update_client.py)  

旧服务会将发送的数字+1后返回 发送update后触发热更新 新服务会将发送的数字+2后返回
```
Integer or Update:   1
b'2'
Integer or Update:   2
b'3'
Integer or Update:   update
b'success'
Integer or Update:   4
b'6'
Integer or Update:   5
b'7'
Integer or Update:   
```