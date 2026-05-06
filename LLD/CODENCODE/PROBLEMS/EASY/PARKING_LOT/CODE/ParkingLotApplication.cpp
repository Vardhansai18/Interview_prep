#include "ParkingLotApplication.h"

namespace parkinglot {

ParkingLotApplication::ParkingLotApplication(std::shared_ptr<ParkingLotService> service)
    : service(service) {}

std::shared_ptr<Ticket> ParkingLotApplication::parkVehicle(std::shared_ptr<Vehicle> vehicle) {
    return service->parkVehicle(vehicle);
}

double ParkingLotApplication::unparkVehicle(std::shared_ptr<Ticket> ticket) {
    return service->unparkVehicle(ticket);
}

} // namespace parkinglot
