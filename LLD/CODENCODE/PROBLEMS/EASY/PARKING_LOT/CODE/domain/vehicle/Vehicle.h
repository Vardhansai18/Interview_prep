#ifndef VEHICLE_H
#define VEHICLE_H

#include <string>
#include "VehicleType.h"

namespace parkinglot {
namespace domain {
namespace vehicle {

class Vehicle {
protected:
    std::string vehicleNumber;
    VehicleType vehicleType;

public:
    Vehicle(const std::string& vehicleNumber, VehicleType vehicleType);
    virtual ~Vehicle() = default;

    std::string getVehicleNumber() const;
    VehicleType getVehicleType() const;
};

} // namespace vehicle
} // namespace domain
} // namespace parkinglot

#endif // VEHICLE_H
