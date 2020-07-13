####介绍Erlang RunTime System（下文中用ERTS代替）
ERTS是一个复杂的系统，具有许多相互依赖的组件。
它以非常便携的方式编写，因此它能在小至微型计算机，
大至TB级内存的多核系统上运行。 
为了能够让应用程序充分优化，你不仅需要了解你的应用程序，
还需要对ERTS本身有透彻的了解。
####1.1 ERTS和 the Erlang Runtime System
本书说的ERTS指任何Erlang Runtime System，包括使用OTP或不使用OTP等实现上的差别（待翻译）
####1.2 怎么读这本书
在本书的第二部分中，我们将研究如何为您的应用程序调整运行时系统，以及如何对应用程序和运行时系统进行概要分析和调试。为了真正知道如何调整系统，您还需要了解系统。
在本书的Part I中，您将深入了解系统运行期的工作方式。Part I的以下各章将单独介绍系统的每个组件。在不全面了解其他组件如何实现的情况下，您应该能够阅读这些章节中的任何一章，但是您将需要有每个组件的基本理解。本介绍性章节的其余部分应为您提供足够的基本理解和词汇，以便您可以按照自己喜欢的顺序在第一部分的其余各章之间进行切换。
如果你有时间，请按顺序阅读本书。对Erlang和ERTS的特定单词或本书中的以特定方式使用的单词，通常会在在首次出现时进行解释。当你了解词汇表时，在对特定概念有疑问时，可以把Part I作为参考。
（反正就是说每一章都独立，随便读，看不懂了回来看第一章）
####1.3 ERTS
在本文中，对ERTS的主要组件进行了基本概述，并需要一些词汇来理解以下各章中每个组件的更详细说明。
##### 1.3.1 Erlang节点(ERTS)
启动Elixir或Erlang应用程序或系统时，真正启动的是Erlang节点。 该节点运行Erlang RunTime系统和虚拟机BEAM。 （或者可能是Erlang的另一种实现方式（请参见第1.4节））。
您的应用程序代码将在Erlang节点中运行，并且该节点的所有层都将影响应用程序的性能。 我们将研究组成一个节点的层堆栈。 这将帮助您了解在不同环境中运行系统的选项。
用面向对象的术语来说，一个Erlang节点是Erlang Runtime System类的对象。 Java世界中的等于JVM实例。
Elixir / Erlang代码的所有运算都在一个节点内完成。 一个Erlang节点在一个OS进程中运行，并且您可以在一台计算机上运行多个Erlang节点。
根据Erlang OTP文档，节点实际上是一个已命名的正在执行的运行时系统。也就是说，如果您启动时未通过命令行提供名称,您将拥有一个运行时，但没有节点。 在这样的系统中，Erlang的is_alive返回false。

    192:workdir yimo$ erl
    Erlang/OTP 20 [erts-9.3] [source] [64-bit] [smp:8:8] [ds:8:8:10] [async-threads:10] [hipe] [kernel-poll:false]
    Eshell V9.3  (abort with ^G)
    1> is_alive().
    false
    
    192:workdir yimo$ erl -name abc
    Erlang/OTP 20 [erts-9.3] [source] [64-bit] [smp:8:8] [ds:8:8:10] [async-threads:10] [hipe] [kernel-poll:false]
    Eshell V9.3  (abort with ^G)
    (abc@192.168.0.104)1> is_alive().
    true

运行时系统本身对术语的使用并不严格。 即使您没有为其命名，也可以获得该节点的名称。 


    192:workdir yimo$ erl
    Erlang/OTP 20 [erts-9.3] [source] [64-bit] [smp:8:8] [ds:8:8:10] [async-threads:10] [hipe] [kernel-poll:false]
    
    Eshell V9.3  (abort with ^G)
    1> node().
    nonode@nohost
在本书中，我们将使用术语"节点"来表示运行时的任何运行实例，无论是否为其指定名称。
#####1.3.2执行环境中的层
您的程序（应用程序）将在一个或多个节点上运行，并且程序的性能不仅取决于您的应用程序代码，还取决于ERTS堆栈中代码下方的所有层。 在图1.1中，您可以看到ERTS堆栈，其中在一台计算机上运行了两个Erlang节点。

