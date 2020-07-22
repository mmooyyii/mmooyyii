#### PostgreSQL插件开发-3 基于gossip的多副本储存
本文重点在于插件，所以选择了实现简单的gossip协议。
把协议实现换成raft或者multi-paxos就能实现靠谱的冗余储存。

加入节点：

流言传播：

选择

参考代码：[citus](https://github.com/citusdata/citus)