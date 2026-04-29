#include <iostream>
#include <memory>
#include <vector>
using namespace std;

// -------------------- Abstract Base Class --------------------
class Payment {
public:
    virtual void pay(double amount) = 0;
    virtual ~Payment() {} // Important for proper cleanup via base pointer
};

// -------------------- Concrete Implementations --------------------
class CardPayment : public Payment {
public:
    void pay(double amount) override {
        cout << "[CardPayment] Processing card payment of $" << amount << endl;
    }
};

class UPIPayment : public Payment {
public:
    void pay(double amount) override {
        cout << "[UPIPayment] Processing UPI payment of $" << amount << endl;
    }
};

class PayPalPayment : public Payment {
public:
    void pay(double amount) override {
        cout << "[PayPalPayment] Processing PayPal payment of $" << amount << endl;
    }
};

// -------------------- New Feature (Added WITHOUT modifying existing code) --------------------
class CryptoPayment : public Payment {
public:
    void pay(double amount) override {
        cout << "[CryptoPayment] Processing crypto payment of $" << amount << endl;
    }
};

// -------------------- Payment Processor (Closed for Modification) --------------------
class PaymentProcessor {
public:
    void processPayment(Payment& paymentMethod, double amount) {
        paymentMethod.pay(amount);
    }
};

// -------------------- Main --------------------
int main() {
    PaymentProcessor processor;

    // Create different payment methods
    CardPayment card;
    UPIPayment upi;
    PayPalPayment paypal;
    CryptoPayment crypto;

    cout << "---- Individual Payments ----" << endl;
    processor.processPayment(card, 100.0);
    processor.processPayment(upi, 200.0);
    processor.processPayment(paypal, 300.0);
    processor.processPayment(crypto, 400.0);

    cout << "\n---- Using Polymorphism (Collection) ----" << endl;

    // Polymorphic usage
    vector<unique_ptr<Payment>> payments;
    payments.push_back(make_unique<CardPayment>());
    payments.push_back(make_unique<UPIPayment>());
    payments.push_back(make_unique<PayPalPayment>());
    payments.push_back(make_unique<CryptoPayment>());

    for (auto& payment : payments) {
        processor.processPayment(*payment, 500.0);
    }

    return 0;
}