
using sizeOfFuncType = int (*)();
#include <iostream>
using namespace std;
struct Obj{
    Obj(sizeOfFuncType func):func(func){}
    sizeOfFuncType func;

    void run(){
        cout << (*func)()<<endl;
    }
};

template <sizeOfFuncType sizeOfFunc>
Obj *MAKECACHENODE(){return new Obj(sizeOfFunc);};
