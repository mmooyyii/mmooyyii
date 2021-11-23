#include <iostream>
#include "set"
#include "string"
#include <bits/stdc++.h>

using namespace std;


void scanLib() {
//  scan a b c
    int a, b, c;
    cin >> a >> b >> c;

//  scan a vector
    int m;
    cin >> m;
    vector<int> v(m);
    for (int i = 0; i < m; i++) cin >> v[i];
}

int main() {
    int loop, target;
    cin >> loop >> target;
    vector<vector<int>> ls;
    int l, r, w, now, mi, ma;
    while (loop--) {
        cin >> l >> r >> w;
        ls.push_back({l, r, w});
    }
    sort(ls.begin(), ls.end());
    set<vector<int>> pre = {{1, 100000000, -100000000}};
    int ret = 1000000000;
    for (int idx = 0; idx < ls.size(); idx++) {
        set<vector<int>> tmp;
        l = ls[idx][0];
        r = ls[idx][1];
        w = ls[idx][2];
        for (auto &p: pre) {
            now = p[0];
            mi = p[1];
            ma = p[2];
            if (now == target) {
                ret = min(ret, ma - mi);
            } else if (now >= l) {
                if (tmp.find({now, mi, ma}) == tmp.end()) {
                    tmp.insert({now, mi, ma});
                }
                if (tmp.find({r, min(mi, w), max(ma, w)}) == tmp.end()) {
                    tmp.insert({r, min(mi, w), max(ma, w)});
                }
            }
        }
        pre = tmp;
    }
    for (auto &p: pre) {
        now = p[0];
        mi = p[1];
        ma = p[2];
        if (now == target) {
            ret = min(ret, ma - mi);
        }
    }
    if (ret == -200000000) {
        cout << 0 << endl;
    } else {
        cout << ret << endl;
    }
    return 0;
}

//int main() {
//    set<int> tmp = {1};
//    auto a = tmp.find(2);
//    if (a == tmp.end()) {
//        cout << 1;
//    }
//    return 0;
//}