本质是memmove比正常情况慢很多, 而且既不是cpu cache的问题, 也不是内存随机读写性能的问题.
不知道怎么解释了.

下面的代码也超时, 而本地运行
```c
#include<stdio.h>

// 引用自 https://github.com/torvalds/linux/blob/8ab2afa23bd197df47819a87f0265c0ac95c5b6a/arch/x86/boot/compressed/string.c#L53
// 删除了其中如果内存没有重叠就使用memcpy的逻辑
void *memmove2(void *dest, const void *src, size_t n)
{
	unsigned char *d = dest;
	const unsigned char *s = src;
	while (n-- > 0)
		d[n] = s[n];
	return dest;
}

// 这是c,不是c++
int main() {
    int a[100000];
    int size = 0;
    for (size = 100000; size > 10; size--) {
        memmove2(a, a + 1, size - 1);
    }
    // for (size = 100000; size > 10; size--) {
    //     memcpy(a, b, size - 1);
    // }
    for (int i = 0; i < size; i++) {
        printf("%d",a[i]);
    }
}
```