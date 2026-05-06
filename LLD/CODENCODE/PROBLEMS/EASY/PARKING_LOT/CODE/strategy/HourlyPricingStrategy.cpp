#include "HourlyPricingStrategy.h"

namespace parkinglot {
namespace strategy {

HourlyPricingStrategy::HourlyPricingStrategy(double ratePerHour)
    : ratePerHour(ratePerHour) {}

double HourlyPricingStrategy::calculatePrice(std::shared_ptr<Ticket> ticket) {
    auto duration = std::chrono::duration_cast<std::chrono::hours>(
        ticket->getExitTime() - ticket->getEntryTime()
    );
    
    long hours = duration.count();
    
    // Minimum 1 hour charge
    return std::max(hours, 1L) * ratePerHour;
}

} // namespace strategy
} // namespace parkinglot
