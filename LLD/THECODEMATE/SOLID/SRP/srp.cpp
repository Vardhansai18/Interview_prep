#include <iostream>
using namespace std;

// -------------------- Order --------------------
class Order {
public:
    string item;
    string customerName;
    bool isDelivery;

    Order(string item, string customerName, bool isDelivery)
        : item(item), customerName(customerName), isDelivery(isDelivery) {}
};

// -------------------- Chef --------------------
class Chef {
public:
    void prepareOrder(const Order& order) {
        cout << "Chef is preparing " << order.item << endl;
    }
};

// -------------------- Waiter --------------------
class Waiter {
public:
    void serveOrder(const Order& order) {
        cout << "Waiter is serving " << order.item
             << " to " << order.customerName << endl;
    }
};

// -------------------- Delivery Agent --------------------
class DeliveryAgent {
public:
    void deliverOrder(const Order& order) {
        cout << "Delivery Agent is delivering " << order.item
             << " to " << order.customerName << "'s home" << endl;
    }
};

// -------------------- Restaurant (Coordinator) --------------------
class Restaurant {
private:
    Chef chef;
    Waiter waiter;
    DeliveryAgent deliveryAgent;

public:
    void processOrder(const Order& order) {
        chef.prepareOrder(order);

        if (order.isDelivery) {
            deliveryAgent.deliverOrder(order);
        } else {
            waiter.serveOrder(order);
        }
    }
};

// -------------------- Main --------------------
int main() {
    Restaurant restaurant;

    // Dine-in order
    Order dineInOrder("Pasta", "Alice", false);
    restaurant.processOrder(dineInOrder);

    cout << "------------------" << endl;

    // Delivery order
    Order deliveryOrder("Pizza", "Bob", true);
    restaurant.processOrder(deliveryOrder);

    return 0;
}