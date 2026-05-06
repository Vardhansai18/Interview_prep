#ifndef TICKET_H
#define TICKET_H

#include <string>
#include <memory>
#include <chrono>
#include "../parking/ParkingSpot.h"
#include "../vehicle/Vehicle.h"

namespace parkinglot {
namespace domain {
namespace ticket {

using namespace parkinglot::domain::parking;
using namespace parkinglot::domain::vehicle;
using TimePoint = std::chrono::system_clock::time_point;

class Ticket {
private:
    std::string ticketId;
    std::shared_ptr<ParkingSpot> spot;
    std::shared_ptr<Vehicle> vehicle;
    TimePoint entryTime;
    TimePoint exitTime;
    double charges;
    bool closed;

    static std::string generateUUID();

public:
    Ticket(std::shared_ptr<ParkingSpot> spot, std::shared_ptr<Vehicle> vehicle);
    
    void closeTicket(double charges);
    void setExitTime(const TimePoint& exitTime);
    
    // Getters
    std::string getTicketId() const;
    std::shared_ptr<ParkingSpot> getSpot() const;
    std::shared_ptr<Vehicle> getVehicle() const;
    TimePoint getEntryTime() const;
    TimePoint getExitTime() const;
    double getCharges() const;
    bool isClosed() const;
};

} // namespace ticket
} // namespace domain
} // namespace parkinglot

#endif // TICKET_H
