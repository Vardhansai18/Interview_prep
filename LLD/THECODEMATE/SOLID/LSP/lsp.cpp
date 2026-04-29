#include <iostream>
#include <vector>
#include <memory>
using namespace std;

// -------------------- Base Class --------------------
class Vehicle {
public:
    // Common behavior for ALL vehicles
    virtual void move() = 0;

    virtual ~Vehicle() {}
};

// -------------------- Engine-based Vehicles --------------------
class EngineVehicle : public Vehicle {
public:
    virtual void startEngine() = 0;
};

// -------------------- Car --------------------
class Car : public EngineVehicle {
public:
    void startEngine() override {
        cout << "Car engine started" << endl;
    }

    void move() override {
        cout << "Car is driving on the road" << endl;
    }
};

// -------------------- Bicycle --------------------
class Bicycle : public Vehicle {
public:
    void move() override {
        cout << "Bicycle is pedaling on the road" << endl;
    }
};

// -------------------- Client Functions --------------------

// Works for ALL vehicles (LSP satisfied)
void travel(Vehicle* v) {
    v->move();
}

// Only works for engine vehicles
void startJourney(EngineVehicle* ev) {
    ev->startEngine();
}

// -------------------- Main --------------------
int main() {
    // Create objects
    Car car;
    Bicycle bicycle;

    cout << "---- Travel (All Vehicles) ----" << endl;
    travel(&car);
    travel(&bicycle);

    cout << "\n---- Engine Start (Only Engine Vehicles) ----" << endl;
    startJourney(&car);
    // startJourney(&bicycle); ❌ Not allowed (compile-time safety)

    cout << "\n---- Polymorphism with Collection ----" << endl;

    vector<unique_ptr<Vehicle>> vehicles;
    vehicles.push_back(make_unique<Car>());
    vehicles.push_back(make_unique<Bicycle>());

    for (auto& v : vehicles) {
        v->move(); // Safe substitution
    }

    return 0;
}