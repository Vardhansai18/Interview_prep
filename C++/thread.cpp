#include <iostream>
using namespace std;

// Base class
class Payment {
public:
    virtual void pay() {
        cout << "Processing generic payment\n";
    }
};

// Derived class 1
class CreditCard : public Payment {
public:
    void pay() override {   // 👈 override
        cout << "Payment done using Credit Card\n";
    }
};

// Derived class 2
class UPI : public Payment {
public:
    void pay() override {   // 👈 override
        cout << "Payment done using UPI\n";
    }
};

class DebitCard : public Payment {
public:
    void pay() override {   // 👈 override
        cout << "Payment done using Credit Card\n";
    }
};

int main() {
    Payment* p1 = new CreditCard();
    Payment* p2 = new UPI();

    p1->pay();  // CreditCard version
    p2->pay();  // UPI version

    delete p1;
    delete p2;

    return 0;
}