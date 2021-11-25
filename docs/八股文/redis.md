请有感情地朗读并背诵全文


下文中的代码出自 redis-5.0.7

- Redis 有哪些数据结构，分别有什么使用场景？


    String Hash List Set SortedSet

- Redis ZSET 相同 score 如何排序？

    
    
- 在爬虫中，如何使用 Redis 做 URL 去重？
- Redis 是否支持事务？ NO
- Redis 中的 WATCH 命令是做什么的？ 
- Redis 是如何保证高可用的？
- 如何使用 Redis 来实现分布式锁？Redlock？

    
    1. Get the current time.
    2. … All the steps needed to acquire the lock …
    3. Get the current time, again.
    4. Check if we are already out of time, or if we acquired the lock fast enough.
    5. Do some work with your lock.
    
    http://antirez.com/news/101
    
- Redis 是单线程还是多线程？为什么这么设计？
    
    
    单线程 IO密集 不需要锁 networking.c 多路复用
    
- Redis 中的字符串对象和 C 语言中的字符串有什么区别？

        
       字符串长度 使用内存 flag 数据
       分为 sdshdr8 sdshdr16 sdshdr32 sdshdr64，可以省下len，alloc的一点点内存
       struct __attribute__ ((__packed__)) sdshdr8 {
        uint8_t len; /* used */
        uint8_t alloc; /* excluding the header and null terminator */
        unsigned char flags; /* 3 lsb of type, 5 unused bits */
        char buf[];
        };

- Redis 中是如何实现链表的？
- Redis 中是如何实现字典的？
- Redis 中的字典是如何进行动态扩容的？
- Redis 中的跳表是如何实现的？
- STR/LIST/HASH/SET/ZSET 底层都是使用什么数据结构实现的？
- ZSET 什么时候使用 Ziplist 实现，什么时候使用 Skiplist 实现？
- ZSET 为什么不用 BST/AVL/B-Tree/红黑树，而使用跳表？
- Redis 的过期键删除策略是什么？                            
- Redis 的主从服务器是如何同步过期键的？
- AOF 和 RDB 持久化有什么区别？
- Redis 的主从是如何进行同步的？
- 如何解决长时间使用后 AOF 文件过大的问题？
- Redis 的哨兵机制是如何实现的？
- Redis 的集群方案有哪些？
- Redis 的整体架构是什么样的，从客户端发出命令，到客户端接收到结果，这整个流程是什么样的？
- Redis 是如何实现 LRU 机制的？

    redisObject里有一个24bit的数据存LRU time
    

- Redis 是如何实现 LFU 机制的？
