场景：1千万用户，1千万视频，以下需求都不需要绝对准确。
用户每次查询权重最高的30个视频，看过的视频不包括在内

```postgresql
create extension hll;
CREATE TABLE app_user(uid int primary key,history hll);
CREATE TABLE video(uuid int primary key,weight float);
insert into app_user(history) select hll_empty() from generate_series(1, 10000000);
insert into video(weight) select random() from generate_series(1, 10000000);
create index video_weight_btree on video (weight);
```

```postgresql
// 用户123 看视频999
update app_user set history = hll_add(history,hll_hash_integer(999)) where uid = 123;
// 查视频
explain (analyse,verbose,costs )
select uuid
from video,
     app_user
where app_user.uid = 123
  and hll_ne(hll_add(app_user.history, hll_hash_integer(video.uuid)), app_user.history)
order by weight desc
limit 30;

Limit  (cost=0.87..6.96 rows=30 width=12) (actual time=0.063..0.117 rows=30 loops=1)
"  Output: video.uuid, video.weight"
  ->  Nested Loop  (cost=0.87..1351777.71 rows=6666666 width=12) (actual time=0.062..0.112 rows=30 loops=1)
"        Output: video.uuid, video.weight"
        Inner Unique: true
"        Join Filter: hll_ne(hll_add(app_user.history, hll_hash_integer(video.uuid, 0)), app_user.history)"
        Rows Removed by Join Filter: 4
        ->  Index Scan Backward using video_weight_btree on public.video  (cost=0.44..951769.25 rows=20000000 width=12) (actual time=0.012..0.046 rows=34 loops=1)
"              Output: video.uuid, video.weight"
        ->  Materialize  (cost=0.43..8.46 rows=1 width=4) (actual time=0.001..0.001 rows=1 loops=34)
              Output: app_user.history
              ->  Index Scan using app_user_pkey on public.app_user  (cost=0.43..8.45 rows=1 width=4) (actual time=0.022..0.023 rows=1 loops=1)
                    Output: app_user.history
                    Index Cond: (app_user.uid = 123)
Planning Time: 0.135 ms
Execution Time: 0.169 ms
```

当某用户看过当视频越来越多当时候：
如用户123看了排名前100000的视频后，Join Filter 变大，导致查询时间急剧增加。
```
explain (analyse,verbose,costs)
select uuid
from video,
     app_user
where app_user.uid = 123
  and hll_ne(hll_add(app_user.history, hll_hash_integer(video.uuid)), app_user.history)
order by weight desc
limit 30;


Limit  (cost=0.88..6.96 rows=30 width=12) (actual time=2151.065..2190.377 rows=30 loops=1)
  ->  Nested Loop  (cost=0.88..1351777.71 rows=6666666 width=12) (actual time=2151.063..2190.361 rows=30 loops=1)
"        Join Filter: hll_ne(hll_add(app_user.history, hll_hash_integer(video.uuid, 0)), app_user.history)"
        Rows Removed by Join Filter: 101745
        ->  Index Scan Backward using video_weight_btree on video  (cost=0.44..951769.25 rows=20000000 width=12) (actual time=0.032..543.213 rows=101775 loops=1)
        ->  Materialize  (cost=0.44..8.46 rows=1 width=4) (actual time=0.000..0.000 rows=1 loops=101775)
              ->  Index Scan using app_user_pkey on app_user  (cost=0.44..8.46 rows=1 width=4) (actual time=0.493..0.503 rows=1 loops=1)
                    Index Cond: (uid = 123)
Planning Time: 0.678 ms
Execution Time: 2190.426 ms

```
优化
```postgresql
查询用户123已经看过的视频数量乘以一个系数代码其中视频在高比重视频中的比例，本例中为0.9,实际中该系数可通过分析用户习惯得到
select (hll_cardinality(history) * 0.9 ):: int from app_user where uid = 123; 
得 88844
explain analyse select min(weight),max(weight) from (select weight from video limit 30 offset 88844) as t;
Aggregate  (cost=1369.59..1369.60 rows=1 width=16) (actual time=20.941..20.941 rows=1 loops=1)
  ->  Limit  (cost=1368.68..1369.14 rows=30 width=8) (actual time=20.926..20.932 rows=30 loops=1)
        ->  Seq Scan on video  (cost=0.00..308109.00 rows=20000000 width=8) (actual time=0.021..15.178 rows=88874 loops=1)
Planning Time: 0.119 ms
Execution Time: 20.962 ms
得 weight范围是 0.028885601292149232 and 0.9318815333595332

explain (analyse,verbose ,costs)
select uuid
from video,
     app_user
where app_user.uid = 123
  and hll_ne(hll_add(app_user.history, hll_hash_integer(video.uuid)), app_user.history) and
      weight between 0.028885601292149232 and 0.9318815333595332
order by weight desc
limit 30;

Limit  (cost=0.88..7.61 rows=30 width=12) (actual time=0.278..23.182 rows=30 loops=1)
"  Output: video.uuid, video.weight"
  ->  Nested Loop  (cost=0.88..1354792.29 rows=6032361 width=12) (actual time=0.278..23.170 rows=30 loops=1)
"        Output: video.uuid, video.weight"
        Inner Unique: true
"        Join Filter: hll_ne(hll_add(app_user.history, hll_hash_integer(video.uuid, 0)), app_user.history)"
        Rows Removed by Join Filter: 1305
        ->  Index Scan Backward using video_weight_btree on public.video  (cost=0.44..992842.11 rows=18097086 width=12) (actual time=0.014..2.597 rows=1335 loops=1)
"              Output: video.uuid, video.weight"
              Index Cond: ((video.weight >= '0.028885601292149232'::double precision) AND (video.weight <= '0.9318815333595332'::double precision))
        ->  Materialize  (cost=0.44..8.46 rows=1 width=4) (actual time=0.000..0.000 rows=1 loops=1335)
              Output: app_user.history
              ->  Index Scan using app_user_pkey on public.app_user  (cost=0.44..8.46 rows=1 width=4) (actual time=0.150..0.151 rows=1 loops=1)
                    Output: app_user.history
                    Index Cond: (app_user.uid = 123)
Planning Time: 0.151 ms
Execution Time: 23.222 ms
```
Join Filter显著下降，性能提高了50倍，且精度也没有损失，如果使用能使Join Filter变得更小的系数，查询效率会更快。