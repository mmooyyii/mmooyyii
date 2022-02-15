#include <bits/stdc++.h>

using namespace std;


void fast_read() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

int m_uf[100001];
class UnionFind {
  int m_count;
 public:
  explicit UnionFind(int n) {
      for (int i = 0; i < n; i++) m_uf[i] = i;
      m_count = n;
  }

  int Find(int a) {
      if (m_uf[a] != a) m_uf[a] = Find(m_uf[a]);
      return m_uf[a];
  }

  void Union(int i, int j) {
      int a = Find(i), b = Find(j);
      if (a != b) m_count -= 1;
      m_uf[a] = b;
  }

  int Count() const {
      return m_count;
  }
};


class SegmentTree {
  vector<int> m_data;
  vector<int> m_tree;
 public:
  explicit SegmentTree(vector<int> &data) {
      m_data = data;
      m_tree.resize(m_data.size() * 4);
      for (int i = 0; i < m_data.size(); i++)
          m_tree[i + m_data.size()] = m_data[i];
      for (int i = (int)m_data.size() - 1; i > 0; i--)
          m_tree[i] = m_merge(m_tree[i * 2], m_tree[i * 2 + 1]);
  }
  static int m_merge(int a, int b) {
      return max(a, b);
  }
  void set(int idx, int val) {
      int left, right;
      m_data[idx] = val;
      int pos = idx + (int)m_data.size();
      m_tree[pos] = val;
      while (pos) {
          left = pos;
          right = pos;
          if (pos & 1) left = pos - 1;
          else right = pos + 1;
          pos >>= 1;
          m_tree[pos] = m_merge(m_tree[left], m_tree[right]);
      }
  }

  int range(int left, int right) {
      int ret = 0;
      left += (int)m_data.size();
      right += (int)m_data.size();
      while (left <= right) {
          if (left & 1) {
              ret = m_merge(ret, m_tree[left]);
              left += 1;
          }
          if (!(right & 1)) {
              ret = m_merge(ret, m_tree[right]);
              right -= 1;
          }
          left >>= 1;
          right >>= 1;
      }
      return ret;
  }
};