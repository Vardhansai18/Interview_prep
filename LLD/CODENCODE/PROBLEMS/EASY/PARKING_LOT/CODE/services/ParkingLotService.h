#ifndef PARKING_LOT_SERVICE_H
#define PARKING_LOT_SERVICE_H

#include <vector>
#include <unordered_map>
#include <memory>
#include <mutex>
#include "../domain/parking/ParkingFloor.h"
#include "../domain/parking/ParkingSpot.h"
#include "../domain/ticket/Ticket.h"
#include "../domain/vehicle/Vehicle.h"
#include "../domain/vehicle/VehicleType.h"
#include "../strategy/PricingStrategy.h"
#include "../exception/ParkingException.h"

namespace parkinglot {
namespace services {

using namespace parkinglot::domain::parking;
using namespace parkinglot::domain::ticket;
using namespace parkinglot::domain::vehicle;
using namespace parkinglot::strategy;
using namespace parkinglot::exception;

class ParkingLotService {
private:
    std::unordered_map<std::string, std::shared_ptr<Ticket>> activeTickets;
    std::vector<std::shared_ptr<ParkingFloor>> parkingFloors;
    std::shared_ptr<PricingStrategy> pricingStrategy;
    std::mutex serviceMutex;

    std::shared_ptr<ParkingSpot> getAvailableParkingSpot(VehicleType vehicleType);

public:
    ParkingLotService(const std::vector<std::shared_ptr<ParkingFloor>>& parkingFloors,
                      std::shared_ptr<PricingStrategy> pricingStrategy);
    
    std::shared_ptr<Ticket> parkVehicle(std::shared_ptr<Vehicle> vehicle);
    double unparkVehicle(std::shared_ptr<Ticket> ticket);
    void setPricingStrategy(std::shared_ptr<PricingStrategy> pricingStrategy);
};

} // namespace services
} // namespace parkinglot

#endif // PARKING_LOT_SERVICE_H
