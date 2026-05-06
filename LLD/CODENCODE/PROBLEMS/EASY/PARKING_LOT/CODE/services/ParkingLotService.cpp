#include "ParkingLotService.h"

namespace parkinglot {
namespace services {

ParkingLotService::ParkingLotService(
    const std::vector<std::shared_ptr<ParkingFloor>>& parkingFloors,
    std::shared_ptr<PricingStrategy> pricingStrategy)
    : parkingFloors(parkingFloors), pricingStrategy(pricingStrategy) {}

std::shared_ptr<Ticket> ParkingLotService::parkVehicle(std::shared_ptr<Vehicle> vehicle) {
    std::shared_ptr<ParkingSpot> spot = getAvailableParkingSpot(vehicle->getVehicleType());
    
    if (!spot->parkVehicle(vehicle)) {
        throw ParkingException("Parking spot was taken concurrently");
    }
    
    auto ticket = std::make_shared<Ticket>(spot, vehicle);
    
    {
        std::lock_guard<std::mutex> lock(serviceMutex);
        activeTickets[ticket->getTicketId()] = ticket;
    }
    
    return ticket;
}

double ParkingLotService::unparkVehicle(std::shared_ptr<Ticket> ticket) {
    {
        std::lock_guard<std::mutex> lock(serviceMutex);
        
        if (activeTickets.find(ticket->getTicketId()) == activeTickets.end()) {
            throw ParkingException("Invalid ticket: " + ticket->getTicketId());
        }
    }
    
    ticket->setExitTime(std::chrono::system_clock::now());
    double charges = pricingStrategy->calculatePrice(ticket);
    ticket->closeTicket(charges);
    ticket->getSpot()->removeVehicle();
    
    {
        std::lock_guard<std::mutex> lock(serviceMutex);
        activeTickets.erase(ticket->getTicketId());
    }
    
    return ticket->getCharges();
}

std::shared_ptr<ParkingSpot> ParkingLotService::getAvailableParkingSpot(VehicleType vehicleType) {
    // Return any available spot (policy can be improved later)
    for (const auto& parkingFloor : parkingFloors) {
        for (const auto& spot : parkingFloor->getParkingSpots()) {
            if (spot->getVehicleType() == vehicleType && spot->isSpotAvailable()) {
                return spot;
            }
        }
    }
    
    throw ParkingException("No spot available for vehicle type");
}

void ParkingLotService::setPricingStrategy(std::shared_ptr<PricingStrategy> pricingStrategy) {
    std::lock_guard<std::mutex> lock(serviceMutex);
    this->pricingStrategy = pricingStrategy;
}

} // namespace services
} // namespace parkinglot
