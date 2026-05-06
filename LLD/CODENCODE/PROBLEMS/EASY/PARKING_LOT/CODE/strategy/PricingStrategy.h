#ifndef PRICING_STRATEGY_H
#define PRICING_STRATEGY_H

#include <memory>
#include "../domain/ticket/Ticket.h"

namespace parkinglot {
namespace strategy {

using namespace parkinglot::domain::ticket;

class PricingStrategy {
public:
    virtual ~PricingStrategy() = default;
    virtual double calculatePrice(std::shared_ptr<Ticket> ticket) = 0;
};

} // namespace strategy
} // namespace parkinglot

#endif // PRICING_STRATEGY_H
