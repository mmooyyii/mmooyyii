#include <bits/stdc++.h>
#include <ext/pb_ds/assoc_container.hpp>

using namespace std;
using namespace __gnu_pbds;

void fast_read() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

// 允许重复数据
struct node {
  int x, tim;
  bool operator<(node o) const {
      if (x != o.x)return x < o.x;
      else return tim < o.tim;
  }
};

typedef tree<node, null_type, less<>, rb_tree_tag, tree_order_statistics_node_update> ordered_set;

int tim = 0;

int main() {
    ordered_set s;
    s.insert({1, tim++});
    s.insert({2, tim++});
    s.insert({2, tim++});
    s.insert({100, tim++});
    cout << s.size() << endl; // 4 允许重复数据
    cout << s.find_by_order(3)->x << endl; // 100 取rank, 从0开始
    cout << s.order_of_key({2, -1}) << endl; // 1  通过val取rank(有几个小于r_key)
    cout << s.order_of_key({2, int(1e9)}) << endl; // 3 通过val取rank(有几个小于等于r_key)
    cout << ((s.find_by_order(s.order_of_key({2, -1}))->x) == 2) << endl; // true 判断是否在set中,如果不允许重复,直接find即可
}