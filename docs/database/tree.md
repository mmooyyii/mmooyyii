关系型数据库中存放树结构的一种办法-闭包表

        
```sql
CREATE TABLE tree(self INT,parent INT,distance INT);
```
self代表本节点，parent是本节点向上distance代的节点

        1           
       / 
      2   
     / \   
    3   4  

比如上图应该存为下表所示，表的空间复杂度是O(nlogn)

    +------+--------+----------+
    | self | parent | distance |
    +------+--------+----------+
    |    1 |      1 |        0 |
    |    2 |      2 |        0 |
    |    3 |      3 |        0 |
    |    4 |      4 |        0 |
    |    2 |      1 |        1 |
    |    3 |      1 |        2 |
    |    3 |      2 |        1 |
    |    4 |      1 |        2 |
    |    4 |      2 |        1 |
    +------+--------+----------+

```sql
// 导入数据
INSERT INTO tree VALUES ( 1,1,0 ),( 2,2,0 ),( 3,3,0 ),( 4,4,0 ),( 2,1,1 ),( 3,1,2 ),( 3,2,1 ),( 4,1,2 ),( 4,2,1 );

查询节点1所有子节点
SELECT self FROM tree WHERE parent = 1 AND self != 1;

// 查询节点2下一级的节点
SELECT self FROM tree WHERE parent = 2 AND distance = 1;

// 查询节点4到节点1的路径
SELECT parent FROM tree WHERE self = 4 ORDER BY distance DESC;

// 在节点1的上方插入节点5
BEGIN;
INSERT INTO tree VALUES (5,5,0);
INSERT INTO tree(self,parent,distance) SELECT self, 5 ,distance + 1 FROM tree WHERE parent = 1;
COMMIT;

// 删除节点2
DELETE FROM tree;
INSERT INTO tree VALUES ( 1,1,0 ),( 2,2,0 ),( 3,3,0 ),( 4,4,0 ),( 2,1,1 ),( 3,1,2 ),( 3,2,1 ),( 4,1,2 ),( 4,2,1 );
BEGIN;
UPDATE tree SET distance = distance - 1 FROM
(SELECT self,distance AS dist FROM tree WHERE parent = 2) AS t2 
WHERE tree.self=t2.self AND tree.distance > t2.dist;
DELETE FROM tree WHERE self = 2 OR parent = 2;
COMMIT;
```
