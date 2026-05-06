#ifndef PRICING_STRATEGY_H
#define PRICING_STRATEGY_H

#include "../models/VehicleType.h"

/**
 * PricingStrategy Interface (Abstract Base Class)
 * 
 * Purpose: Define contract for all pricing strategies
 * 
 * SOLID Principles Applied:
 * 
 * 1. Interface Segregation Principle (ISP):
 *    - Small, focused interface with only one method
 *    - Clients only depend on what they need
 *    - No "fat interface" with unused methods
 * 
 * 2. Open/Closed Principle (OCP):
 *    - Open for extension: Create new pricing strategies
 *    - Closed for modification: Don't change interface
 * 
 * 3. Dependency Inversion Principle (DIP):
 *    - High-level module (ParkingLotService) depends on abstraction (this interface)
 *    - Not on concrete implementations (SimplePricingStrategy, HourlyPricingStrategy)
 *    - Easy to swap pricing strategies at runtime
 * 
 * Design Pattern: STRATEGY PATTERN
 * 
 * What is Strategy Pattern?
 * - Define family of algorithms (pricing strategies)
 * - Encapsulate each one
 * - Make them interchangeable
 * 
 * Benefits:
 * - Add new pricing without changing existing code
 * - Runtime strategy switching (hourly, daily, monthly)
 * - Easy testing (mock pricing strategies)
 * 
 * Example Strategies You Could Add:
 * - HourlyPricingStrategy: Charge per hour
 * - DailyPricingStrategy: Flat daily rate
 * - WeekendPricingStrategy: Different rates on weekends
 * - PeakHourPricingStrategy: Higher rates during rush hours
 * - MembershipPricingStrategy: Discounts for members
 */

class PricingStrategy {
public:
    // Virtual destructor: Essential for proper cleanup through base pointer
    virtual ~PricingStrategy() = default;
    
    /**
     * Calculate parking fee
     * 
     * Parameters:
     * - vehicleType: Type of vehicle (affects pricing)
     * - durationInHours: How long vehicle was parked
     * 
     * Returns: Fee amount in currency units
     * 
     * Pure virtual function (= 0):
     * - Makes this class abstract (can't instantiate)
     * - Forces derived classes to implement
     * - Ensures all strategies have this method
     */
    virtual double calculatePrice(VehicleType vehicleType, double durationInHours) const = 0;
};

#endif // PRICING_STRATEGY_H
