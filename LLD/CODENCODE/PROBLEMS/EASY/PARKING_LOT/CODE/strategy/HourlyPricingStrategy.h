#ifndef HOURLY_PRICING_STRATEGY_H
#define HOURLY_PRICING_STRATEGY_H

#include "PricingStrategy.h"
#include <algorithm>

namespace parkinglot {
namespace strategy {

class HourlyPricingStrategy : public PricingStrategy {
private:
    double ratePerHour;

public:
    explicit HourlyPricingStrategy(double ratePerHour);
    ~HourlyPricingStrategy() override = default;
    
    double calculatePrice(std::shared_ptr<Ticket> ticket) override;
};

} // namespace strategy
} // namespace parkinglot

#endif // HOURLY_PRICING_STRATEGY_H
