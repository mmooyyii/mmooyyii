#### 看minio的代码的笔记(版本是2.7.0)

### 存文件
http handle 写在 cmd/web-handler.go
一通检查后，通过`objInfo, err := putObject(context.Background(), bucket, object, pReader, opts)`存入文件
其中pReader是上传的文件的handle

objectAPI.PutObject这个对象会根据不同的环境选择不同的实现函数，使用linux文件系统的会使用FSObject
其他的还有亚马逊的S3,hadoop的hdfs, 微软的azure等对应的实现。

启动时分4个盘`./minio server /data1 /data2 /data3 /data4`  
把data3，data4删了，文件依然能成功下载，这要归功于minio的纠错码  

纠错码的实现： todo  

单机纠错码模式下的文件系统   
在data1按存入的对象的路径创建文件夹，最后一级中存part.1-part.n和一个xl.json描述对象的属性   
创建一个内容是"123"的小文件，minio依然如上述说明创建对象，所以minio在储存海量小文件时，不会对数个小文件进行压缩，
在存大量小文件时，[minio应该没有什么优势](http://slack.minio.org.cn/question/47).  

单机非纠错码模式下的文件系统  
在data1按存入的对象的路径创建文件夹，最后一级存一个文件，这也太简单了吧，那我也是写过对象存储的人了。  

#### pkg/auth  一些帐号的生成与检测的api
生成access和secret的算法可以关注一下,写法简单,在极大多数情况下可以保证不重复    

检验SecretKey时使用了ConstantTimeCompare，无论输入的密码长度，都会用相同的时间返回  
比如 密码是 "123456" ，我输入密码是 "9"，一般人写这个代码很可能在判断 "1" != "9"的时候就return False了  
而实际上这样会导致让攻击者通过检测密码的返回时间判断前N位的正确性  
假设检测一位的时间是1秒  
我输入 "129457"，函数的返回时间是 2秒  
我输入 "113457"，函数的返回时间是 1秒  
那么我就能判断出密码的前2位是"12"  
具体可以看[timing attack](https://codahale.com/a-lesson-in-timing-attacks/)

##### pkg/bpool  似乎是一个用于缓存溢出的byte的东西，暂时不太清楚具体用途
make的第三个参数，声明数据结构的容量，会在第一次分配内存的时候留出声明的空间，而不赋具体的值。  

