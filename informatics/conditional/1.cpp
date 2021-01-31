#include <iostream>

using namespace std;

int c[1001];

int main(){
    long long n;
    cin >> n;
    for (int i = 2; i <= 1000; ++i)
    {
        if(n % i == 0){
            c[i]++;
            n /= i;
            --i;
        }
    }

    int cnt = 1;
    for(int i = 0; i < 1001; ++i){
        if(c[i] != 0){
            cnt *= (c[i] + 1);
        }
    }

    cout << cnt;
    

    return 0;
}