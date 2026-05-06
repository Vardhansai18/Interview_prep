#ifndef PARKING_LOT_APPLICATION_H
#define PARKING_LOT_APPLICATION_H

#include <memory>
#include "services/ParkingLotService.h"
#include "domain/ticket/Ticket.h"
#include "domain/vehicle/Vehicle.h"

namespace parkinglot {

using namespace parkinglot::services;
using namespace parkinglot::domain::ticket;
using namespace parkinglot::domain::vehicle;

class ParkingLotApplication {
private:
    std::shared_ptr<ParkingLotService> service;

public:
    explicit ParkingLotApplication(std::shared_ptr<ParkingLotService> service);
    
    std::shared_ptr<Ticket> parkVehicle(std::shared_ptr<Vehicle> vehicle);
    double unparkVehicle(std::shared_ptr<Ticket> ticket);
};

} // namespace parkinglot

#endif // PARKING_LOT_APPLICATION_H
