#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
typedef unsigned long long ull;

class Vechile{
    public:
    virtual void drive()
    {
        cout << "Vechile Drive" << endl;
    }
};




class Car: public Vechile{
    public:
    void drive() override
    {
        cout << "Car Drive" << endl;
    }
};


class Bus: public Vechile{
    public:
    void drive()
    {
        cout << "Bus Drive" << endl;
    }
};


class Bike: public Vechile{
    public:
    void drive()
    {
        cout << "Bike Drive" << endl;
    }
};

class VechileFactory{
    public:
    Vechile* createVechile( string type )
    {
        if( type == "car" )
        {
            return new Car();
        }
        else if( type == "bike" )
        {
            return new Bike();
        }
        else if( type == "Bus" )
        {
            return new Bus();
        }
        return nullptr;
    }

};


int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    VechileFactory factory;

    Vechile *bus1 = factory.createVechile("Bus");
    bus1->drive();

    

    return 0;
}