#include <iostream>
using namespace std;

// -------------------- Abstraction --------------------
class Device {
public:
    virtual void turnOn() = 0;
    virtual ~Device() {}
};

// -------------------- Low-Level Modules --------------------
class Light : public Device {
public:
    void turnOn() override {
        cout << "Light is ON\n";
    }
};

class Fan : public Device {
public:
    void turnOn() override {
        cout << "Fan is ON\n";
    }
};

class AC : public Device {
public:
    void turnOn() override {
        cout << "AC is ON\n";
    }
};

// -------------------- High-Level Module --------------------
class Switch {
private:
    Device* device;  // ✅ Depends on abstraction

public:
    // Dependency Injection via constructor
    Switch(Device* d) : device(d) {}

    void operate() {
        device->turnOn();
    }
};

// -------------------- Main --------------------
int main() {
    Light light;
    Fan fan;
    AC ac;

    cout << "Using Light:\n";
    Switch s1(&light);
    s1.operate();

    cout << "\nUsing Fan:\n";
    Switch s2(&fan);
    s2.operate();

    cout << "\nUsing AC:\n";
    Switch s3(&ac);
    s3.operate();

    return 0;
}