#ifndef CAR_H
#define CAR_H

#include "Vehicle.h"

namespace parkinglot {
namespace domain {
namespace vehicle {

class Car : public Vehicle {
public:
    explicit Car(const std::string& vehicleNumber);
    ~Car() override = default;
};

} // namespace vehicle
} // namespace domain
} // namespace parkinglot

#endif // CAR_H
