#### PostgreSQL插件开发-2 拓展类型
对于一些16进制的编号，如A10302BB，在存储时的理想情况是存为2701329083，占用4个字节，但是这样的话可读性就下降了，
如果存成varchar(8)又占用了较多的空间。
理想情况是像inet类型一样,两者兼得。
```
yimo=# create table test(a inet, b text);
CREATE TABLE
yimo=# insert into test values ('192.168.31.24'::inet,'192.168.31.24');
INSERT 0 1
yimo=# select pg_column_size(a),pg_column_size(b) from test;
 pg_column_size | pg_column_size 
----------------+----------------
              7 |             14
(1 row)
yimo=# select * from test;
        a        |       b       
-----------------+---------------
 192.168.31.24   | 192.168.31.24
(1 row)
```
对于上述的编号，我们希望能有一种新的数据类型，用于存储16进制的数据。
```
yimo=# create table test(a pg_hex,b text);
CREATE TABLE
yimo=# insert into test values ('A10302BB'::hex,'A10302BB');
INSERT 0 1
yimo=# select * from test;
     a    |     b         
----------+-----------
 A10302BB |  A10302BB
(1 row)
```

创建扩展类型
```
CREATE TYPE hex (
  INTERNALLENGTH = VARIABLE,
  INPUT = hex_in,
  OUTPUT = hex_out,
  receive = hex_recv,
  send = hex_send,
  STORAGE = default
);
```

INPUT && OUTPUT 外部文本形式与内部格式之间的转换

RECEIVE && SEND 外部二进制形式与内部形式的转换  

INTERNALLENGTH && STORAGE 数据的长度与储存方式


重载操作符   


使用索引：  
对于btree，hash索引

对于gin，gist索引


本文中的所有代码可以在[这里](https://github.com/mmooyyii/pg_plugin_demo/tree/master/hello_world)找到。  
参考代码：[HyperLogLog](https://github.com/citusdata/postgresql-hll)  [RoaringBitMap](https://github.com/ChenHuajun/pg_roaringbitmap)


