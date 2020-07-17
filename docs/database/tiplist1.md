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
如用户123看了排名前10000的视频后，Join Filter 变大，导致查询时间急剧增加。
```
explain (analyse,verbose,costs)
select uuid
from video,
     app_user
where app_user.uid = 123
  and hll_ne(hll_add(app_user.history, hll_hash_integer(video.uuid)), app_user.history)
order by weight desc
limit 30;

Limit  (cost=0.88..6.96 rows=30 width=12) (actual time=196.657..201.304 rows=30 loops=1)
"  Output: video.uuid, video.weight"
  ->  Nested Loop  (cost=0.88..1351777.71 rows=6666666 width=12) (actual time=196.654..201.295 rows=30 loops=1)
"        Output: video.uuid, video.weight"
        Inner Unique: true
"        Join Filter: hll_ne(hll_add(app_user.history, hll_hash_integer(video.uuid, 0)), app_user.history)"
        Rows Removed by Join Filter: 10206
        ->  Index Scan Backward using video_weight_btree on public.video  (cost=0.44..951769.25 rows=20000000 width=12) (actual time=0.008..14.983 rows=10236 loops=1)
"              Output: video.uuid, video.weight"
        ->  Materialize  (cost=0.44..8.46 rows=1 width=4) (actual time=0.000..0.000 rows=1 loops=10236)
              Output: app_user.history
              ->  Index Scan using app_user_pkey on public.app_user  (cost=0.44..8.46 rows=1 width=4) (actual time=0.115..0.116 rows=1 loops=1)
                    Output: app_user.history
                    Index Cond: (app_user.uid = 123)
Planning Time: 0.115 ms
Execution Time: 201.335 ms

```
优化
```postgresql
查询用户123已经看过的视频数量乘以一个系数代码其中视频在高比重视频中的比例，本例中为0.9,实际中该系数可通过分析用户习惯得到
select (hll_cardinality(history) * 0.9 ):: int from app_user where uid = 123; 
得 9010
explain (analyse,verbose ,costs) select min(weight),max(weight) from (select weight from video order by weight desc offset 9010 limit 30) as t;
Aggregate  (cost=431.09..431.10 rows=1 width=16) (actual time=7.127..7.127 rows=1 loops=1)
"  Output: min(video.weight), max(video.weight)"
  ->  Limit  (cost=429.21..430.64 rows=30 width=8) (actual time=7.094..7.118 rows=30 loops=1)
        Output: video.weight
        ->  Index Only Scan Backward using video_weight_btree on public.video  (cost=0.44..951769.25 rows=20000000 width=8) (actual time=0.011..6.570 rows=9040 loops=1)
              Output: video.weight
              Heap Fetches: 9040
Planning Time: 0.110 ms
Execution Time: 7.146 ms
得 weight范围是 0.999539910164355 and 0.999541571044567 (postgresql的offset真是不行)

explain (analyse,verbose ,costs)
select uuid
from video,
     app_user
where app_user.uid = 123
  and hll_ne(hll_add(app_user.history, hll_hash_integer(video.uuid)), app_user.history) and
      weight between 0.999539910164355 and 0.999541571044567
order by weight desc
limit 30;

Limit  (cost=156.68..156.71 rows=12 width=12) (actual time=0.617..0.617 rows=0 loops=1)
"  Output: video.uuid, video.weight"
  ->  Sort  (cost=156.68..156.71 rows=12 width=12) (actual time=0.616..0.616 rows=0 loops=1)
"        Output: video.uuid, video.weight"
        Sort Key: video.weight DESC
        Sort Method: quicksort  Memory: 25kB
        ->  Nested Loop  (cost=5.24..156.46 rows=12 width=12) (actual time=0.613..0.613 rows=0 loops=1)
"              Output: video.uuid, video.weight"
"              Join Filter: hll_ne(hll_add(app_user.history, hll_hash_integer(video.uuid, 0)), app_user.history)"
              Rows Removed by Join Filter: 30
              ->  Index Scan using app_user_pkey on public.app_user  (cost=0.44..8.46 rows=1 width=4) (actual time=0.112..0.114 rows=1 loops=1)
"                    Output: app_user.uid, app_user.history"
                    Index Cond: (app_user.uid = 123)
              ->  Bitmap Heap Scan on public.video  (cost=4.81..147.38 rows=36 width=12) (actual time=0.014..0.047 rows=30 loops=1)
"                    Output: video.uuid, video.weight"
                    Recheck Cond: ((video.weight >= '0.999539910164355'::double precision) AND (video.weight <= '0.999541571044567'::double precision))
                    Heap Blocks: exact=30
                    ->  Bitmap Index Scan on video_weight_btree  (cost=0.00..4.80 rows=36 width=0) (actual time=0.009..0.009 rows=30 loops=1)
                          Index Cond: ((video.weight >= '0.999539910164355'::double precision) AND (video.weight <= '0.999541571044567'::double precision))
Planning Time: 0.248 ms
Execution Time: 0.645 ms
```
Join Filter显著下降，性能约提高了30倍，且精度也没有损失，如果使用能使Join Filter变得更小的系数，查询效率会更快。