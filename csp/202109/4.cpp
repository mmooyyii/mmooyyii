// 题目要求精度 0.0001，实际判定时要10个有效数字？
// 这题用python怎么写能过呢？

#include<bits/stdc++.h>

using namespace std;

int a, b;
vector<double> cards;
double memo[(1 << 17)][16 * 5 + 1];

double dp(int status, int coin) {
    if (memo[status][coin] > 0) return memo[status][coin];
    int hand = int(bitset<32>(status).count());
    if ((a - hand) * b <= coin)
        return hand + coin;
    double ans = 0;
    for (int i = 0; i < a; i++) {
        if (status & (1 << i)) {
            ans += dp(status, coin + 1) * cards[i];
        } else {
            ans += dp(status | (1 << i), coin) * cards[i];
        }
    }
    memo[status][coin] = ans;
    return ans;
}

int main() {
    cin >> a >> b;
    fill_n(&memo[0][0], (1 << 17) * (16 * 5 + 1), -1.0);
    for (int i = 0; i < a; i++) {
        double tmp;
        cin >> tmp;
        cards.push_back(tmp);
    }
    printf("%.10lf", dp(0, 0));
}