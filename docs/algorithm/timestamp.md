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
{2021280,ok} 
```

时间戳转日期
```erlang
ts_to_date(Ts) ->
%%  Year month day
    Day = Ts div 86400 + 719468,
    Era = case Day > 0 of true -> Day div 146097;false -> (Day - 146096) div 146097 end,
    Doe = Day - Era * 146097,
    Yoe = (Doe - Doe div 1460 + Doe div 36524 - Doe div 146069) div 365,
    Y = Yoe + Era * 400,
    Doy = Doe - (365 * Yoe + Yoe div 4 - Yoe div 100),
    Mp = (5 * Doy + 2) div 153,
    D = Doy - (154 * Mp + 2) div 5 + 1,
    M = case Mp < 10 of
            true -> 3 + Mp;
            false -> -9 + Mp
        end,
    Date = {case M =< 2 of true -> 1 + Y;false -> Y end, M, D},
%%    hour minute second
    S = Ts rem 86400,
    Time = {S div 3600, S rem 3600 div 60, S rem 60},
    {Date, Time}.
```
