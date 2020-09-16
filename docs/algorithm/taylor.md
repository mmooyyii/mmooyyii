游戏行业中通常会有大量的配置文件
通常来说，配置文件是用图灵不完备的json，yaml等写的
如果需要配置的一条曲线中包含了sin，pow等数学函数，
就需要写一个配置文件的解释器来使用配置了，而且配置的形式也会趋向于Abstract Syntax Tree（AST）

通过taylor展开式，将曲线改成
y = k1 * x ^ n + k2 * x ^ (n-1) ..... kn * x ^ 0的形式，
即可在图灵不完备的配置语言中，完成复杂的曲线配置。

下面代码网上抄的
```python3
import matplotlib.pyplot as plt
import numpy as np
x = np.arange(1, 17, 1)
y = np.array([4.00, 6.40, 8.00, 8.80, 9.22, 9.50, 9.70, 9.86, 10.00, 10.20, 10.32, 9.42, 8.50, 7.55, 6.58, 3.60])
z1 = np.polyfit(x, y, 8)
p1 = np.poly1d(z1)
print(p1)
yvals = p1(x)
plot1 = plt.plot(x, y, '*', label='original values')
plot2 = plt.plot(x, yvals, 'r', label='polyfit values')
plt.xlabel('x axis')
plt.ylabel('y axis')
plt.legend(loc=4)
plt.title('polyfitting')
plt.show()
plt.savefig('p1.png')
```


