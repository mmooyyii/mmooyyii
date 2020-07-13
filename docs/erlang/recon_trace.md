在平时维护线上服务器的时候，常会使用recon_trace:call捕获传递的消息。
但是在消费者模式下，无法确定具体上那台机器消费了某条消息，所以必须在所有计算上都调用recon_trace:call，非常麻烦。

于是我通过使用io_server实现了如下的效果：
```erlang
(a@127.0.0.1) > recon_trace:remote_calls(['b@127.0.0.1','c@127.0.0.1'],{lists,seq,'_'},10).
(b@127.0.0.1) > lists:seq(1).
(c@127.0.0.1) > lists:seq(1).
%% a@127.0.0.1的console中
b@127.0.0.1 18:38:01.195994 <0.88.0>  lists:seq(1)  
c@127.0.0.1 18:38:01.195994 <0.89.0>  lists:seq(1)
```

代码如下，其中注意分发io_server时需要用global模块去注册
```erlang
remote_call(Nodes, {M, F, A}, Max) ->
    IoServer = register_io_server(),
    rpc:multicall(Nodes, recon_trace, remote_called, [{M, F, A}, Max, IoServer], 5000).

remote_clear(Nodes) ->
    rpc:multicall(Nodes, recon_trace, clear, [], 5000).

register_io_server() ->
    Default = recon_default_group_leader,
    global:unregister_name(Default),
    global:unregister_name(group_leader()),
    global:register_name(Default, group_leader()),
    Default.

remote_called({M, F, A}, Max, IoServer) ->
    Formatter = fun(Data) -> [_ | S] = format(Data), atom_to_list(node()) ++ " " ++ S end,
    calls({M, F, A}, Max, [{io_server, global:whereis_name(IoServer)}, {formatter, Formatter}]).
```

为什么recon不提供这个功能呢？  
[作者的回答是:](https://github.com/ferd/recon/issues/81)

I'm afraid this is going to be tricky to make production-safe given the high volume of traces potentially run.
The counter approach works well locally because we have the ability to do backpressure handling like that.
In a distributed setting the backpressure mechanism has to be a bit more sensitive to the distributed ports, 
and that requires doing things a bit more from scratch. 
Especially if the counter is local, you might kill remote nodes before yours even know there's a problem.
I would be tempted to say no to this feature just because it's very hard to make it work safely.

大致意思是说多个节点同用一个io_server太危险，而且计数器不好控制，在生产环境下使用太危险了。
所以上面的代码使用的时候max一定要小，而且io_server所在的机器最好是不运行业务代码的闲置机。