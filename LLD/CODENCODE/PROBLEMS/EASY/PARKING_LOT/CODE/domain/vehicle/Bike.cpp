#include "Bike.h"

namespace parkinglot {
namespace domain {
namespace vehicle {

Bike::Bike(const std::string& vehicleNumber)
    : Vehicle(vehicleNumber, VehicleType::BIKE) {}

} // namespace vehicle
} // namespace domain
} // namespace parkinglot
