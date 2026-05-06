#include "Truck.h"

namespace parkinglot {
namespace domain {
namespace vehicle {

Truck::Truck(const std::string& vehicleNumber)
    : Vehicle(vehicleNumber, VehicleType::TRUCK) {}

} // namespace vehicle
} // namespace domain
} // namespace parkinglot
