在平时维护线上服务器的时候，常会使用recon_trace:call捕获传递的消息。
但是在集群中，很多时候无法确定具体是那台机器处理了某次请求，所以必须开多个console然后在所有机器上都调用recon_trace:call，非常麻烦。

于是我通过使用io_server实现了如下的效果：
```erlang
(a@127.0.0.1) > recon_trace:remote_calls(['b@127.0.0.1','c@127.0.0.1'],{lists,seq,'_'},10).
(b@127.0.0.1) > lists:seq(1).
(c@127.0.0.1) > lists:seq(1).
%% a@127.0.0.1的console中
b@127.0.0.1 18:38:01.195994 <0.88.0>  lists:seq(1)  
c@127.0.0.1 18:38:01.195994 <0.89.0>  lists:seq(1)
```

代码如下：
```erlang
remote_call(Nodes, {M, F, A}, Max) ->
    {ok, IoServer} = recon_io_buffer:start_link(Nodes),
    Formatter = fun(Data) -> [_ | S] = recon_trace:format(Data), erlang:atom_to_list(erlang:node()) ++ " " ++ S end,
    Opt = [{io_server, IoServer}, {formatter, Formatter}],
    {IoServer, rpc:multicall(Nodes, recon_trace, calls, [{M, F, A}, Max, Opt], 5000)}.
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

为了解决上述问题，我又写了recon_io_buffer用于缓存

```erlang
-module(recon_io_buffer).
-author("yimo").
-behaviour(gen_server).
-export([start_link/1]).
-export([init/1, handle_call/3, handle_cast/2, handle_info/2, terminate/2, code_change/3]).
-define(SERVER, ?MODULE).


%% 直接使用IoServer会导致背压式(Back Pressure)的调用，所以这里需要做一个IoServer的buffer，
%% 在高压力的情况下，解除recon_trace:calls,防止对生产环境造成影响


-define(MaxQueueLen, 200).
-record(recon_io_server_state, {
    io,
    remote_nodes,
    queue
}).

start_link(Nodes) ->
    gen_server:start_link(?MODULE, [Nodes], []).

init([Nodes]) ->
    erlang:send_after(100, self(), io),
    {ok, #recon_io_server_state{
        io = group_leader(),
        remote_nodes = Nodes,
        queue = {0, queue:new()}
    }}.

handle_call(stop, From, State = #recon_io_server_state{remote_nodes = Nodes}) ->
    R = rpc:multicall(Nodes, recon_trace, clear, [], 5000),
    gen_server:reply(From, R),
    {stop, normal, State}.

handle_cast(_Request, State = #recon_io_server_state{}) ->
    {noreply, State}.

handle_info({io_request, From, Mref, M}, State = #recon_io_server_state{
    remote_nodes = Nodes,
    queue = {L, Queue}
}) ->
    case L > ?MaxQueueLen of
        false ->
            From ! {io_reply, Mref, ok},
            {noreply, State#recon_io_server_state{
                queue = {L + 1, queue:in({io_request, self(), Mref, M}, Queue)}
            }};
        true ->
            rpc:multicall(Nodes, recon_trace, clear, [], 5000),
            {stop, warning, State}
    end;

handle_info(io, State = #recon_io_server_state{io = Io, queue = {_, Queue}}) ->
    lists:foreach(fun(Msg) -> Io ! Msg end, queue:to_list(Queue)),
    erlang:send_after(100, self(), io),
    {noreply, State#recon_io_server_state{queue = {0, queue:new()}}};

handle_info(_, State) ->
    {noreply, State}.

terminate(warning, #recon_io_server_state{io = Io, queue = {_, Queue}}) ->
    lists:foreach(fun(Msg) -> Io ! Msg end, queue:to_list(Queue)),
    io:format("Quit: high benchmark~n"),
    ok;

terminate(_Reason, _State) ->
    io:format("Quit~n"),
    ok.

code_change(_OldVsn, State = #recon_io_server_state{}, _Extra) ->
    {ok, State}.
```
