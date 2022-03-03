#include <bits/stdc++.h>
using namespace std;

void fast_read() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

#define N 600000
using namespace std;
int n, q;
int x, y, posx, posy;
string op;
int L[N * 30], R[N * 30], fa[N * 30], dep[N * 30];
int root[N * 30];
namespace Persistant_Union_Set {
int cnt;
void build(int &rt, int l, int r) {
    rt = ++cnt;
    if (l == r) {
        fa[rt] = l;
        return;
    }
    build(L[rt], l, ((l + r) >> 1));
    build(R[rt], ((l + r) >> 1) + 1, r);
}
void merge(int last, int &rt, int l, int r, int pos, int Fa) {
    rt = ++cnt;
    L[rt] = L[last], R[rt] = R[last];
    if (l == r) {
        fa[rt] = Fa;
        dep[rt] = dep[last];
        return;
    }
    if (pos <= ((l + r) >> 1)) {
        merge(L[last], L[rt], l, ((l + r) >> 1), pos, Fa);
    } else {
        merge(R[last], R[rt], ((l + r) >> 1) + 1, r, pos, Fa);
    }
}
void update(int rt, int l, int r, int pos) {
    if (l == r) {
        dep[rt]++;
        return;
    }
    if (pos <= ((l + r) >> 1))update(L[rt], l, ((l + r) >> 1), pos);
    else update(R[rt], ((l + r) >> 1) + 1, r, pos);
}
int query(int rt, int l, int r, int pos) {
    if (l == r)return rt;
    if (pos <= ((l + r) >> 1))return query(L[rt], l, ((l + r) >> 1), pos);
    else return query(R[rt], ((l + r) >> 1) + 1, r, pos);
}
int find(int rt, int pos) {
    int now = query(rt, 1, n, pos);
    if (fa[now] == pos)return now;
    return find(rt, fa[now]);
}
}

using namespace Persistant_Union_Set;

map<int, int> group_memo;

// 可持久化并查集... 怎么这么难?
// 这里抄的 https://www.luogu.com.cn/problem/solution/P3402

int main() {
    fast_read();
    cin >> q >> n;
    build(root[0], 1, n);
    int age = 0;
    int group = n;
    group_memo[age] = n;
    for (int _ = 1; _ <= q; _++) {
        cin >> op;
        if (op == "PUSH") {
            cin >> x >> y;
            age += 1;
            root[age] = root[age - 1];
            posx = find(root[age], x);
            posy = find(root[age], y);
            if (fa[posx] != fa[posy]) {
                if (dep[posx] > dep[posy]) {
                    swap(posx, posy);
                }
                merge(root[age - 1], root[age], 1, n, fa[posx], fa[posy]);
                if (dep[posx] == dep[posy]) {
                    update(root[age], 1, n, fa[posy]);
                }
                group -= 1;
            }
            group_memo[age] = group;
        } else {
            root[age] = root[age - 1];
            group = group_memo[age - 1];
            age -= 1;
        }
        cout << group << endl;
    }
    return 0;
}