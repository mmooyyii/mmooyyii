推荐列表新需求：在N天内看过的视频不包括在内
由于PostgreSQL的offset无法优化，这个当用户视频累积越来越多时，
会导致查询缓慢。这个需求算是好消息。

新需求2：每个视频针对不同用户应该有不同的权重

新需求3：加大用户量至10亿