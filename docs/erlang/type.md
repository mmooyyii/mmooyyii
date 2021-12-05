如何在erlang中判断一个变量的类型

在erlang中，似乎没有一个函数可以返回erlang的变量的type？
如果自己实现，一种比较简单的方式是
```erlang
type(List) when is_list(List)-> list;
type(Tuple) when is_tuple(Tuple)-> tuple;
......
```
使用erlang:term_to_binary/1也能判断term的类型
erlang:term_to_binary/1得到的binary的结构如下

| 1|  1| N |
|:----:|:----:|:----:|
| 131  | Tag |     Data  |

比如
```erlang
(a@127.0.0.1)16> erlang:term_to_binary("1").
<<131,107,0,1,49>>
(a@127.0.0.1)17> erlang:term_to_binary("11231231313").
<<131,107,0,11,49,49,50,51,49,50,51,49,51,49,51>>
```
Tag = 107 表示数据类型是List
具体的tag-type对应关系看[这里](http://erlang.org/doc/apps/erts/erl_ext_dist.html)