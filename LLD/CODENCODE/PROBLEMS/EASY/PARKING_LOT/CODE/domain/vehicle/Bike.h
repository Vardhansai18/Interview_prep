#ifndef BIKE_H
#define BIKE_H

#include "Vehicle.h"

namespace parkinglot {
namespace domain {
namespace vehicle {

class Bike : public Vehicle {
public:
    explicit Bike(const std::string& vehicleNumber);
    ~Bike() override = default;
};

} // namespace vehicle
} // namespace domain
} // namespace parkinglot

#endif // BIKE_H
