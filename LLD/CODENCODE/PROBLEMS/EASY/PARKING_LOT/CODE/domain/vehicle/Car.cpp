#include "Car.h"

namespace parkinglot {
namespace domain {
namespace vehicle {

Car::Car(const std::string& vehicleNumber)
    : Vehicle(vehicleNumber, VehicleType::CAR) {}

} // namespace vehicle
} // namespace domain
} // namespace parkinglot
