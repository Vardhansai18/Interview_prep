#ifndef SIMPLE_PRICING_STRATEGY_H
#define SIMPLE_PRICING_STRATEGY_H

#include "PricingStrategy.h"

/**
 * SimplePricingStrategy (Concrete Implementation)
 * 
 * Purpose: Basic hourly pricing with different rates per vehicle type
 * 
 * SOLID Principles Applied:
 * 
 * 1. Single Responsibility:
 *    - Only calculates price using simple hourly formula
 *    - Doesn't handle parking logic or spot management
 * 
 * 2. Liskov Substitution:
 *    - Can be used anywhere PricingStrategy is expected
 *    - Doesn't change expected behavior
 * 
 * Pricing Logic:
 * - Bike:  $2 per hour
 * - Car:   $5 per hour
 * - Truck: $10 per hour
 * 
 * Formula: fee = hourlyRate * (duration rounded up to nearest hour)
 * 
 * Why round up duration?
 * - Industry standard: Partial hours count as full hour
 * - Example: 1.5 hours = 2 hours charged
 * - Using ceil() function for rounding up
 * 
 * Future Enhancements:
 * - Add minimum charge (e.g., 1 hour even for 10 minutes)
 * - Add maximum daily cap
 * - Add surge pricing during peak hours
 * - Add discount for longer parking (daily/weekly rates)
 */

#include <cmath>  // for ceil() function

class SimplePricingStrategy : public PricingStrategy {
private:
    // Hourly rates for each vehicle type (in currency units)
    const double BIKE_HOURLY_RATE = 2.0;
    const double CAR_HOURLY_RATE = 5.0;
    const double TRUCK_HOURLY_RATE = 10.0;

public:
    /**
     * Calculate price based on vehicle type and duration
     * 
     * Implementation: Simple hourly calculation
     * Time Complexity: O(1)
     * 
     * Example Calculation:
     * - Car parked for 2.3 hours
     * - Rounded up: 3 hours
     * - Fee: 3 * $5 = $15
     */
    double calculatePrice(VehicleType vehicleType, double durationInHours) const override {
        // Round up to nearest hour (partial hour = full hour)
        int hours = static_cast<int>(std::ceil(durationInHours));
        
        // Ensure minimum 1 hour charge (even for < 1 hour)
        if (hours < 1) {
            hours = 1;
        }
        
        // Calculate fee based on vehicle type
        double hourlyRate = 0.0;
        
        switch (vehicleType) {
            case VehicleType::BIKE:
                hourlyRate = BIKE_HOURLY_RATE;
                break;
            case VehicleType::CAR:
                hourlyRate = CAR_HOURLY_RATE;
                break;
            case VehicleType::TRUCK:
                hourlyRate = TRUCK_HOURLY_RATE;
                break;
            default:
                hourlyRate = CAR_HOURLY_RATE;  // Default to car rate
        }
        
        return hourlyRate * hours;
    }
};

#endif // SIMPLE_PRICING_STRATEGY_H
