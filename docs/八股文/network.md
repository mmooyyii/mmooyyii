#### TCP/IP协议栈层次结构

#### TCP三次握手需要知道的细节点

#### TCP四次挥手需要知道的细节点(CLOSE_WAIT、TIME_WAIT、MSL)

#### TCP与UDP的区别与适用场景

    1. 在中国不建议在公网中使用udp
    2. 在处理视频流时可能会使用udp
    3. 基于udp的协议 quic，kcp
    4. 其他情况下一律使用tcp

#### linux常见网络模型详解(select、poll与epoll)

#### epoll_event结构中的epoll_data_t的fd与ptr的使用场景

#### 异步的connect函数如何编写

#### select函数可以检测网络异常吗？

#### epoll的水平模式和边缘模式

#### 如何将socket设置成非阻塞的(创建时设置与创建完成后设置)，非阻塞socket与阻塞的socket在收发数据上的区别

#### send/recv(read/write)返回值大于0、等于0、小于0的区别

#### 如何编写正确的收数据代码与发数据代码

#### 发送数据缓冲区与接收数据缓冲区如何设计

#### socket选项SO_SNDTIMEO和SO_RCVTIMEO

#### socket选项TCP_NODELAY

#### socket选项SO_REUSEADDR和SO_REUSEPORT（Windows平台与linux平台的区别）

    端口复用  linux下有负载均衡，windows下没有

#### socket选项SO_LINGER

#### tcp fast open

#### 拥塞控制

shutdown与优雅关闭 socket选项SO_KEEPALIVE 关于错误码EINTR 如何解决tcp粘包问题（粘包👮‍出动！） 信号SIGPIPE与EPIPE错误码 gethostbyname阻塞与错误码获取问题
心跳包的设计技巧（保活心跳包与业务心跳包） 断线重连机制如何设计 如何检测对端已经关闭 如何清除无效的死链（端与端之间的线路故障） 定时器的不同实现及优缺点 http协议的具体格式 http head、get与post方法的细节
http代理、socks4代理与socks5代理如何编码实现

