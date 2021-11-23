主要记录一下windows 环境下的idea插件开发的流程

安装docker

https://github.com/JetBrains/intellij-platform-plugin-template
里有一个绿色的按钮,叫Use the template,按一下, 把该填的东西填一下, 你的repositories里就有了一个模板项目

git clone你的项目, 用idea打开它

打开Project Structure -> Project SDK -> Add Sdk -> Download Jdk, 装一个11以上的jdk.

然后打开 setting-> Build,Execution,Deployment-> BuildTools -> Gradle -> Gradle JVM换成11以上的jdk

按idea右上角的Run, 运行 Run Qodana,然后开始等,我等了30分钟,
虽然不知道具体在做什么,但是建议开全局代理吧
如果中间你等急了想重开,记得把docker ps里面那个jetbrains/qodana:latest的进程kill了,不然再次启动会报错.
如果你不会写kotlin,可用拿这段时间去学一下 https://learnxinyminutes.com/docs/zh-cn/kotlin-cn/
