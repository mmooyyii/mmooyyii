```cpp

#include <bits/stdc++.h>
#include<immintrin.h>

using namespace std;

class Solution {
 public:
  __attribute__((no_sanitize_address, no_sanitize_memory))
  __attribute__((target("avx2")))
  vector<int> twoSum(vector<int> &n, int target) {
      auto tar = _mm256_set1_epi32(target);
      for (int i = 0; i + 7 < n.size(); i += 8) {
          for (int ii = 0; ii < 8; ii++)
              for (int jj = ii + 1; jj < 8; jj++)
                  if (n[i + ii] + n[i + jj] == target)
                      return {i + ii, i + jj};
          __m256i aa = _mm256_set_epi32(n[i], n[i + 1], n[i + 2], n[i + 3], n[i + 4], n[i + 5], n[i + 6], n[i + 7]);
          for (int j = i + 8; j < n.size(); j++) {
              __m256i ans = _mm256_cmpeq_epi32(_mm256_add_epi32(aa, _mm256_set1_epi32(n[j])), tar);
              for (int k = 0; k < 8; ++k) {
                  if (((int *)&ans)[k]) return {7 - k + i, j};
              }
          }
      }
      for (int i = n.size() / 8 * 8; i < n.size(); i++) {
          for (int j = i + 1; j < n.size(); j++) {
              if (n[i] + n[j] == target) return {i, j};
          }
      }
      return {0, 0};
  }
};

int main() {
    vector<int> a = {1, 2, 3, 4};
    Solution().twoSum(a, 4);
}

```

用avx2指令集做一做[LeetCode第一题](https://leetcode.cn/problems/two-sum/)  
即使是O(n^2)的时间复杂度也只要40ms.

[查看更多的avx2指令](https://www.intel.com/content/www/us/en/docs/intrinsics-guide/index.html#ig_expand=0,1,5627&techs=AVX2)
