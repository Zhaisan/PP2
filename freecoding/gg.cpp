#include <iostream>
using namespace std;
int main(){
    int n;
    cin >> n;
    int k;
    cin >> k;
    int a[n];
    for(int i = 0; i < n; i++){
        cin >> a[i];
    }
    for(int i = 0; i < n; i++){
        if(a[i] == k){
            cout << i << " ";
        }
        else{
            cout << "Отсутствует";
        }
    }

    return 0;
}