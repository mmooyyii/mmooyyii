class Solution:
    def abbreviateProduct(self, left: int, right: int) -> str:

        if right - left < 100:
            ans = 1
            for i in range(left, right + 1):
                ans *= i
            ans = str(ans)
            tmp = ans.strip('0')
            zero = len(ans) - len(tmp)
            if len(tmp) <= 10:
                ans = tmp + "e" + str(zero)
            else:
                ans = tmp[:5] + "..." + tmp[-5:] + "e" + str(zero)
            return ans

        def five(n):
            ans = 0
            while n % 5 == 0:
                n //= 5
                ans += 1
            return ans

        zero = 0
        for n in range(left, right + 1):
            zero += five(n)
        prefix = 1
        for n in range(left, right + 1):
            prefix *= n
            prefix = int(str(prefix)[:80])

        suffix = 1
        for n in range(left, right + 1):
            suffix *= n
            suffix = int(str(suffix).rstrip('0')[-20:])
        return str(prefix)[:5] + "..." + str(suffix)[-5:] + "e" + str(zero)


print(Solution().abbreviateProduct(6, 563035))
print(Solution().abbreviateProduct(18, 237575))
print(Solution().abbreviateProduct(3940, 836328))
print(Solution().abbreviateProduct(2965, 574229))
print(Solution().abbreviateProduct(6148, 215373))
