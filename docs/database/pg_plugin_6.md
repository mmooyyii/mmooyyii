#### PostgreSQL插件开发-6 冒泡排序

```
create table bb(a int);
insert into bb select random() * 10000 from generate_series(1,10000);
explain analyse select * from bb order by a;

Sort  (cost=933.52..962.21 rows=11475 width=4) (actual time=5.292..7.030 rows=10000 loops=1)
  Sort Key: a
  Sort Method: quicksort  Memory: 853kB
  ->  Seq Scan on bb  (cost=0.00..159.75 rows=11475 width=4) (actual time=0.015..2.145 rows=10000 loops=1)
Planning Time: 0.086 ms
Execution Time: 7.808 ms
```


参考代码：[pgnso](https://github.com/dmitigr/pgnso)