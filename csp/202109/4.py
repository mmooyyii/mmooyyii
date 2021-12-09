import sys

sys.setrecursionlimit(int(1e9))


def input():
    return sys.stdin.readline().strip('\n')


def cin_int_ls():
    return list(map(int, input().split()))


def cin_int():
    return int(input())


def main():
    def dp(status, coin):
        if memo[status][coin] != -1:
            return memo[status][coin]
        hand = bin(status).count('1')
        if (a - hand) * b <= coin:
            memo[status][coin] = hand + coin
            return hand + coin
        ans = 0
        for i, p in enumerate(cards):
            if status & (1 << i):
                ans += dp(status, coin + 1) * p
            else:
                ans += dp(status | (1 << i), coin) * p
        memo[status][coin] = ans
        return ans

    a, b = cin_int_ls()
    memo = [[-1 for _ in range(a * b + 5)] for _ in range(1 << a)]
    cards = list(map(float, input().split()))
    print(dp(0, 0))


import time

start = time.time()
main()
print(time.time() - start)

"""
#include <bits/stdc++.h>
using namespace std;

int a, b;
vector<double> cards;
double memo[(1 << 17)][16 * 5 + 1];

double dp(int status, int coin) {
    if (memo[status][coin] > 0) return memo[status][coin];
    int hand = int(bitset<32>(status).count());
    if ((a - hand) * b <= coin)
        return double(hand + coin);
    double ans = 0;
    for (int i = 0; i < a; i++) {
        if (status & (1 << i)) {
            ans += (dp(status, coin + 1) * cards[i]);
        } else {
            ans += (dp(status | (1 << i), coin) * cards[i]);
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
    cout << dp(0, 0) << endl;
}


"""