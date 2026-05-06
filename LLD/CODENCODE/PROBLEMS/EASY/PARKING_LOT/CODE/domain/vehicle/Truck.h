#ifndef TRUCK_H
#define TRUCK_H

#include "Vehicle.h"

namespace parkinglot {
namespace domain {
namespace vehicle {

class Truck : public Vehicle {
public:
    explicit Truck(const std::string& vehicleNumber);
    ~Truck() override = default;
};

} // namespace vehicle
} // namespace domain
} // namespace parkinglot

#endif // TRUCK_H
