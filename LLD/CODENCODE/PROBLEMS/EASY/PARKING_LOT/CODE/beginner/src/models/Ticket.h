#ifndef TICKET_H
#define TICKET_H

#include <string>
#include <chrono>
#include <memory>
#include "Vehicle.h"
#include "ParkingSpot.h"

/**
 * Ticket Class
 * 
 * Purpose: Receipt given when vehicle enters parking lot
 * 
 * SOLID Principles Applied:
 * 
 * 1. Single Responsibility:
 *    - Only stores parking session information
 *    - Doesn't calculate fees (that's PricingStrategy's job)
 *    - Doesn't manage spots (that's ParkingSpot's job)
 * 
 * 2. Open/Closed:
 *    - Can extend to add: QR code, barcode, ticket type (hourly/monthly)
 *    - Without modifying existing code
 * 
 * Key Information Stored:
 * - ticketId: Unique identifier
 * - vehicle: Which vehicle is parked
 * - spot: Where it's parked
 * - entryTime: When vehicle entered (for duration calculation)
 * 
 * Design Decisions:
 * 
 * 1. Why store Vehicle* and ParkingSpot*?
 *    - Need to know WHICH vehicle and WHERE it's parked
 *    - When user returns, we validate ticket and locate the vehicle
 * 
 * 2. Why use chrono::system_clock?
 *    - C++ standard for time handling
 *    - Accurate timestamp for fee calculation
 *    - Can calculate duration easily
 * 
 * 3. Why not store exitTime?
 *    - Exit time determined when unparkVehicle() is called
 *    - Ticket is immutable after creation (good practice)
 *    - Service calculates exit time at payment
 */

class Ticket {
private:
    std::string ticketId;                                    // Unique ticket identifier
    Vehicle* vehicle;                                        // Parked vehicle
    ParkingSpot* spot;                                       // Assigned parking spot
    std::chrono::system_clock::time_point entryTime;        // Entry timestamp

public:
    // Constructor: Create ticket when vehicle enters
    Ticket(const std::string& id, Vehicle* v, ParkingSpot* s)
        : ticketId(id), vehicle(v), spot(s) {
        // Record current time as entry time
        entryTime = std::chrono::system_clock::now();
    }
    
    // Getters
    std::string getTicketId() const { return ticketId; }
    Vehicle* getVehicle() const { return vehicle; }
    ParkingSpot* getSpot() const { return spot; }
    std::chrono::system_clock::time_point getEntryTime() const { return entryTime; }
    
    /**
     * Calculate parking duration in hours
     * 
     * Called when vehicle exits to determine fee
     * Returns: Duration in hours (as double for partial hours)
     * 
     * Example:
     * - Entry: 10:00 AM
     * - Exit:  11:30 AM
     * - Duration: 1.5 hours
     */
    double getDurationInHours() const {
        auto now = std::chrono::system_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::minutes>(now - entryTime);
        return duration.count() / 60.0;  // Convert minutes to hours
    }
    
    /**
     * Get formatted entry time as string
     * Useful for display purposes
     */
    std::string getFormattedEntryTime() const {
        std::time_t entryTimeT = std::chrono::system_clock::to_time_t(entryTime);
        return std::ctime(&entryTimeT);
    }
};

#endif // TICKET_H
