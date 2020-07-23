#### PostgreSql插件开发-1 hello,world!

只需要简单的几步，就能完成一个简单的pg插件

1. 给要开发的插件起一个名字
hello_world
2. 创建3个文件

hello_world.control
```
//文件名的组成格式**必须**是「插件名」.control
comment = 'Hello, world!' //插件注释,显示在 \dx的Description列中
default_version = '0.0.1' // 默认版本，这里选择0.0.1
relocatable = true
```
[relocatable参数见postgresql文档35.17.3](https://www.postgresql.org/docs/12/extend-extensions.html#EXTEND-EXTENSIONS-RELOCATION)

hello_world--0.0.1.sql
```
//文件名的组成格式**必须**是「插件名」--「版本号」.sql
//内容非常简单，就是一个helloworld函数，通常pg中的函数用下划线命名法
CREATE FUNCTION hello_world()
RETURNS text
LANGUAGE plpgsql IMMUTABLE STRICT
  AS $$
    BEGIN
    RETURN('Hello, world!');
    END;
  $$;
```
Makefile
```
EXTENSION = hello_world  #插件名
DATA = hello_world--0.0.1.sql #要执行的sql文件

PG_CONFIG = pg_config #pg_config的命令
PGXS := $(shell $(PG_CONFIG) --pgxs) # 查看pgxs路径的命令
include $(PGXS)
```

创建完3个文件后，在Makefile的目录下输入make install即可完成安装
```
YideMacBook-Pro:helloworld yimo$ make install
/bin/sh /usr/local/lib/postgresql/pgxs/src/makefiles/../../config/install-sh -c -d '/usr/local/share/postgresql/extension'
/bin/sh /usr/local/lib/postgresql/pgxs/src/makefiles/../../config/install-sh -c -d '/usr/local/share/postgresql/extension'
/usr/bin/install -c -m 644 .//hello_world.control '/usr/local/share/postgresql/extension/'
/usr/bin/install -c -m 644 .//hello_world--0.0.1.sql  '/usr/local/share/postgresql/extension/'
```


在psql中安装插件，这样一个简单的pg插件就开发完成了。
```
YideMacBook-Pro:helloworld yimo$ psql
psql (12.2)
Type "help" for help.

yimo=# create extension hello_world;
CREATE EXTENSION
yimo=# select hello_world();
  hello_world  
---------------
 Hello, world!
(1 row)

yimo=# \dx
                                        List of installed extensions
     Name      | Version |   Schema   |                             Description                             
---------------+---------+------------+---------------------------------------------------------------------
 hello_world   | 0.0.1   | public     | Hello, world!
 hll           | 2.14    | public     | type for storing hyperloglog data
 pg_trgm       | 1.4     | public     | text similarity measurement and index searching based on trigrams
 pgcrypto      | 1.3     | public     | cryptographic functions
 plpgsql       | 1.0     | pg_catalog | PL/pgSQL procedural language
 postgis       | 3.0.1   | public     | PostGIS geometry, geography, and raster spatial types and functions
 roaringbitmap | 0.5     | public     | support for Roaring Bitmaps
(7 rows)
```

本文中的所有代码可以在[这里](https://github.com/mmooyyii/pg_plugin_demo/tree/master/hello_world)找到。