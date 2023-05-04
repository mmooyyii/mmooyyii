#include "bits/stdc++.h"


// 运行 g++ print.cpp -std=c++20 && ./a.out
// 一个相对简短易懂的, 类似python的print, 用于打印常用的STL容器.
// 主要用了c++20的concept

using namespace std;
template<typename T>
concept is_iterable_v = requires(T t) {
    t.begin();
    t.end();
};

template<typename Iter>
concept is_kv_v = requires(Iter t) {
    t->first;
    t->second;
};

template<typename T>
concept is_tuple_v = requires(T t) { std::get<0>(t); };

template<typename T>
concept is_queue = requires(T t) {
    t.top();
    t.pop();
    t.empty();
};

template<typename T>
auto str(const T &) -> string;

template<int N, typename... T>
auto help(const std::tuple<T...> &tuple) -> std::string {
    if constexpr (N == 0) {
        return std::to_string(std::get<N>(tuple));
    } else {
        return help<N - 1, T...>(tuple) + ", " + str(std::get<N>(tuple));
    }
}

template<typename... T>
auto str(const std::tuple<T...> &t) -> std::string {
    return "{" +
           help<std::tuple_size_v<std::remove_cvref_t<decltype(t)>> - 1, T...>(
                   t) +
           "}";
}

template<typename T1, typename T2>
auto str(const std::pair<T1, T2> &data) -> string {
    return '{' + str(data.first) + ", " + str(data.second) + '}';
}

template<typename T1, typename T2>
auto str_kv(const std::pair<T1, T2> &data) -> string {
    return str(data.first) + ": " + str(data.second);
}

template<typename Iter>
auto str(Iter first, Iter last) -> string {
    string ans;
    if constexpr (std::random_access_iterator<Iter>) {
        for (auto iter = first; iter != last; ++iter)
            ans += str(*iter) + ", ";
        if (not ans.empty())
            ans.pop_back(), ans.pop_back();
        return '[' + ans + ']';
    } else {
        for (auto iter = first; iter != last; ++iter) {
            if constexpr (is_kv_v<Iter>)
                ans += str_kv(*iter) + ", ";
            else
                ans += str(*iter) + ", ";
        }
        if (not ans.empty())
            ans.pop_back(), ans.pop_back();
        return '{' + ans + '}';
    }
}

template<typename T>
auto str(const T &data) -> string {
    if constexpr (std::is_same_v<string, T>) {
        return data;
    } else if constexpr (is_integral_v<T> or is_floating_point_v<T>) {
        return to_string(data);
    } else if constexpr (std::is_same_v<bool, T>) {
        return data ? "true" : "false";
    } else if constexpr (is_iterable_v<T>) {
        return str(data.begin(), data.end());
    } else if constexpr (is_tuple_v<T>) {
        return str(data);
    } else if constexpr (is_same_v<T, const char *>) {
        return std::string(data);
    } else if constexpr (is_queue<T>) {
        auto copy = data;
        auto tmp = vector<typename T::value_type>();
        while (not copy.empty()) {
            tmp.push_back(copy.top());
            copy.pop();
        }
        return str(tmp);
    } else {
        return "(unknown type: " + to_string(reinterpret_cast<int64_t>(&data)) +
               ")";
    }
}

template<typename... T>
auto print(T... a) {
    auto tuple = std::tuple<T...>(a...);
}

template<typename T>
auto print(T a) { std::cout << str(a) << std::endl; }

template<typename Head, typename... T>
auto print(Head head, T... a) {
    std::cout << str(head) << ' ';
    return print(a...);
}


int main() {
    {
        auto a = std::map<std::pair<int, int>, std::vector<float>>();
        a[{1, 2}] = {1.0, 1.1};
        a[{3, 4}] = {2.2, 3.3};
        print(a);
    }
    {
        print(1, 2, 3, 4, "ABC", 1.0, std::vector<int>{1, 2, 3});
    }
    {
        auto a = std::map<int, std::map<int, std::pair<int, int>>>();
        a[1] = {{1, {1, 1}},
                {2, {2, 2}}};
        a[2] = {{99, {3,  3}},
                {2,  {66, 66}}};
        print(a);
    }
    return 0;
}