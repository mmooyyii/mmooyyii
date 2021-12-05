OSX上部分PostgreSQL的插件不能用brew直接安装，大致安装流程在这里记录一下（以hll为例）

* https://github.com/citusdata/postgresql-hll 的release中下载源码
* make中报错，找不到stdio.h
* 找到xcode的lib目录，/Library/Developer/CommandLineTools/SDKs/MacOSX10.14.sdk/usr/include/stdio.h  
我的xcode不是从app store安装的，所以路径有问题。
* 在make打印出的gcc命令中加上 -I {xcode目录}
* 安装完成
