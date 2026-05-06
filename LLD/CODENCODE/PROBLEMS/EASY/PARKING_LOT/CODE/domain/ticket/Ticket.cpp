#include "Ticket.h"
#include <random>
#include <sstream>
#include <iomanip>

namespace parkinglot {
namespace domain {
namespace ticket {

// Simple UUID generator (simplified version)
std::string Ticket::generateUUID() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, 15);
    
    const char* hex = "0123456789abcdef";
    std::stringstream ss;
    
    // Generate a simple UUID-like string
    for (int i = 0; i < 32; ++i) {
        if (i == 8 || i == 12 || i == 16 || i == 20) {
            ss << '-';
        }
        ss << hex[dis(gen)];
    }
    
    return ss.str();
}

Ticket::Ticket(std::shared_ptr<ParkingSpot> spot, std::shared_ptr<Vehicle> vehicle)
    : ticketId(generateUUID()),
      spot(spot),
      vehicle(vehicle),
      entryTime(std::chrono::system_clock::now()),
      charges(0.0),
      closed(false) {}

void Ticket::closeTicket(double charges) {
    this->charges = charges;
    this->closed = true;
}

void Ticket::setExitTime(const TimePoint& exitTime) {
    this->exitTime = exitTime;
}

// Getters
std::string Ticket::getTicketId() const {
    return ticketId;
}

std::shared_ptr<ParkingSpot> Ticket::getSpot() const {
    return spot;
}

std::shared_ptr<Vehicle> Ticket::getVehicle() const {
    return vehicle;
}

TimePoint Ticket::getEntryTime() const {
    return entryTime;
}

TimePoint Ticket::getExitTime() const {
    return exitTime;
}

double Ticket::getCharges() const {
    return charges;
}

bool Ticket::isClosed() const {
    return closed;
}

} // namespace ticket
} // namespace domain
} // namespace parkinglot
