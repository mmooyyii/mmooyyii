时间戳-日期快速转换

在[这里](http://howardhinnant.github.io/date_algorithms.html#civil_from_days)看到一个特别牛逼的日期算法，
应该是完爆大多数语言的标准库了。
```erlang
date_to_ts1({{Y, M, D}, {H, Mm, S}}) ->
    {M_Adj, Carry} = case M >= 3 of true -> {M - 3, 0};_ -> {M + 256 - 3, 1} end,
    Adjust = case Carry of 1 -> 12;_ -> 0 end,
    Y_adj = Y + 4800 - Carry,
    MonthDays = ((M_Adj + Adjust) * 62719 + 769) div 2048,
    Leap_days = Y_adj div 4 - Y_adj div 100 + Y_adj div 400,
    (Y_adj * 365 + Leap_days + MonthDays + (D - 1) - 2472632) * 86400 + (3600 * H + Mm * 60 + S).

date_to_ts2(DateTime) ->
    calendar:datetime_to_gregorian_seconds(DateTime) - 62167219200.

t1() ->
    timer:tc(fun() ->lists:foreach(fun(_) -> date_to_ts1({{2020, 10, 10}, {10, 10, 10}}) end, lists:seq(1, 5000000)) end).
t2() ->
    timer:tc(fun() ->
        lists:foreach(fun(_) -> date_to_ts2({{2020, 10, 10}, {10, 10, 10}}) end, lists:seq(1, 5000000)) end).
```
不使用hipe
```erlang
(abc@127.0.0.1)19> test:t1().
{1276850,ok}
(abc@127.0.0.1)20> test:t2().
{1532480,ok}
```
使用hipe
```erlang
(abc@127.0.0.1)22> test:t1().   
{553229,ok} 
(abc@127.0.0.1)23> test:t2().
{2021280,ok}  （使用hipe时标准库反而更慢了）
```

