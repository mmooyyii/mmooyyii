请问[这个模块](https://github.com/benoitc/mimerl/blob/master/src/mimerl.erl)中的
`mimerl:mimetypes/1`的时间复杂度是多少？O(1),O(logN)还是O(N)?

生成测试代码：
```shell script
echo "n = 100000
print(\"-module(aaa).\n-export([f/1]).\n\")
for i in range(n): print(f\"f({i})->{i};\")
print(f\"f({n})->{n}.\")" | python3 > aaa.erl
```
f(1)和f(100000)的时间相同,当模块中只有一个f(1)->1. 时消耗时间也相同
```erlang
(bb@127.0.0.1)5> timer:tc(fun() ->lists:foreach(fun(_) -> aaa:f(1) end, lists:seq(1, 5000000)) end).
{3283407,ok}
(bb@127.0.0.1)6> timer:tc(fun() ->lists:foreach(fun(_) -> aaa:f(100000) end, lists:seq(1, 5000000)) end). 
{3194389,ok}
```
对于这种参数中有超长字符串的情况，结果也相同。
```erlang
f(1)->1;
f(<<"....">>)->1;  %% 长度约为500000的binary
f([...])->1;  %% 长度约为1000的list
f([...])->1;%% 长度约为200的list,中间有几个匹配的变量，  
f(10000)->1.
```

当上面第4个函数list长度更长时，编译时报错
```erlang
test: function f/1+1535:
  An implementation limit was reached.
  Try reducing the complexity of this function.
  Instruction: {get_list,{x,1022},{x,1023},{x,1024}}
error
```
当匹配的是较复杂的数据结构时结果也相同，代码这里就不写了。而且在例如这种`f({A,A,{A,[B,D]}}) -> 1.`形式的模式匹配也能做到O(1),
根据上述的表现来看，应该是在编译期转换成了类似与DFA的数据结构用于索引模式匹配，同时限制匹配参数的长度，从而达到O(1)的匹配速度。
具体的实现方式等有空看看erlang代码再补充。
erlang模式匹配的原理：
...................