#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
typedef unsigned long long ull;

class PaymentStrategy{
public:
    virtual void Pay(int amount){
        cout << "default Payment" << endl;
    }
};

class UpiPayment : public PaymentStrategy{
public:
    void Pay(int amount) override {
        cout << "UPI Payment of " << amount << " amount"  << endl;
    }
};

class CashPayment : public PaymentStrategy{
public:
    void Pay( int amount ) override {
        cout << "Cash Payment " << amount << " amount"  << endl;
    }
};

class CardPayment : public PaymentStrategy{
public:
    void Pay( int amount ) override {
        cout << "Card Payment "<< amount << " amount"  << endl;
    }
};


class PaymentService{
    public:
    PaymentStrategy* strategy;

    PaymentService( PaymentStrategy* strategy )
    {
        this->strategy = strategy;
    }

    void setStrategy(PaymentStrategy* strategy  )
    {
        this->strategy = strategy;
    }

    void makePayment( int amount )
    {
        strategy->Pay( amount );
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    CardPayment* cardPayment = new CardPayment();

    UpiPayment* upiPayment = new UpiPayment();

    
    PaymentService* paymentService = new PaymentService(cardPayment);

    paymentService->makePayment( 100 );

    paymentService->setStrategy( upiPayment );

    paymentService->makePayment( 200 );




    return 0;
}