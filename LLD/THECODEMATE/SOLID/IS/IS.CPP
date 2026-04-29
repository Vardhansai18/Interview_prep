#include <iostream>
using namespace std;

/*
    ISP: Split large interfaces into smaller, specific ones
*/

// Interface for 2D shapes
class TwoDimensionalShape {
public:
    virtual double calculateArea() = 0;
    virtual ~TwoDimensionalShape() {}
};

// Interface for 3D shapes
class ThreeDimensionalShape {
public:
    virtual double calculateVolume() = 0;
    virtual ~ThreeDimensionalShape() {}
};

/*
    Square → Only 2D
    Should NOT implement volume
*/
class Square : public TwoDimensionalShape {
private:
    double side;

public:
    Square(double s) : side(s) {}

    double calculateArea() override {
        return side * side;
    }
};

/*
    Cuboid → Both 2D + 3D
*/
class Cuboid : public TwoDimensionalShape, public ThreeDimensionalShape {
private:
    double length, width, height;

public:
    Cuboid(double l, double w, double h)
        : length(l), width(w), height(h) {}

    double calculateArea() override {
        return 2 * (length * width + width * height + height * length);
    }

    double calculateVolume() override {
        return length * width * height;
    }
};

int main() {

    // Square (only area)
    Square sq(4);
    cout << "Square Area: " << sq.calculateArea() << endl;

    cout << "----------------------" << endl;

    // Cuboid (area + volume)
    Cuboid cb(2, 3, 4);
    cout << "Cuboid Area: " << cb.calculateArea() << endl;
    cout << "Cuboid Volume: " << cb.calculateVolume() << endl;

    return 0;
}