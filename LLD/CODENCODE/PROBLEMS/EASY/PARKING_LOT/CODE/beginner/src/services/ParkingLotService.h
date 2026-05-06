#ifndef PARKING_LOT_SERVICE_H
#define PARKING_LOT_SERVICE_H

#include "../models/ParkingFloor.h"
#include "../models/Ticket.h"
#include "../models/Vehicle.h"
#include "../strategies/PricingStrategy.h"
#include <vector>
#include <map>
#include <string>
#include <sstream>
#include <iomanip>

/**
 * ParkingLotService (Main Business Logic)
 * 
 * Purpose: Orchestrates all parking operations
 * 
 * SOLID Principles Applied:
 * 
 * 1. Single Responsibility Principle (SRP):
 *    - Manages parking operations (park/unpark)
 *    - Coordinates between floors, spots, and tickets
 *    - Delegates pricing to PricingStrategy
 *    - Doesn't handle UI, persistence, or network
 * 
 * 2. Dependency Inversion Principle (DIP):
 *    - Depends on PricingStrategy abstraction, not concrete class
 *    - Can inject different pricing strategies
 *    - Loose coupling = easy testing and modification
 * 
 * 3. Open/Closed Principle (OCP):
 *    - Can extend with new features (reservations, VIP parking)
 *    - Without modifying core parking logic
 * 
 * Key Responsibilities:
 * - Find available parking spots across floors
 * - Issue tickets when vehicles enter
 * - Process exit and calculate fees
 * - Manage ticket tracking
 * 
 * Data Structures Used:
 * - vector<ParkingFloor*>: All floors in parking lot
 * - map<string, Ticket*>: Quick ticket lookup by ticketId
 * 
 * Why map for tickets?
 * - O(1) average lookup time by ticket ID
 * - Essential for fast exit processing
 * - Alternative: unordered_map for slightly faster lookup
 */

class ParkingLotService {
private:
    std::vector<ParkingFloor*> floors;              // All parking floors
    std::map<std::string, Ticket*> activeTickets;   // Currently parked vehicles
    PricingStrategy* pricingStrategy;                // Pricing algorithm
    int ticketCounter;                               // For generating unique ticket IDs

public:
    /**
     * Constructor
     * 
     * Dependency Injection:
     * - Pricing strategy passed in (not created inside)
     * - Follows Dependency Inversion Principle
     * - Allows different strategies for different parking lots
     */
    ParkingLotService(PricingStrategy* strategy)
        : pricingStrategy(strategy), ticketCounter(1) {}
    
    /**
     * Destructor
     * 
     * Clean up all allocated memory:
     * - All tickets (prevent memory leaks)
     * - All floors (which clean up spots)
     */
    ~ParkingLotService() {
        // Clean up all active tickets
        for (auto& pair : activeTickets) {
            delete pair.second;
        }
        
        // Clean up all floors (floors delete their spots)
        for (auto floor : floors) {
            delete floor;
        }
    }
    
    /**
     * Add a floor to the parking lot
     * 
     * Use Case:
     * - Building parking lot structure
     * - Called during initialization
     */
    void addFloor(ParkingFloor* floor) {
        floors.push_back(floor);
    }
    
    /**
     * Park a vehicle
     * 
     * Flow:
     * 1. Find available spot across all floors
     * 2. If found:
     *    - Park vehicle in spot
     *    - Generate ticket
     *    - Store ticket for later retrieval
     *    - Return ticket to user
     * 3. If not found:
     *    - Return nullptr (lot is full)
     * 
     * Time Complexity: O(F * S) where F = floors, S = spots per floor
     * 
     * Optimization Ideas:
     * - Maintain available spot list per floor
     * - Use priority queue for nearest spot
     * - Separate queues for each vehicle type
     */
    Ticket* parkVehicle(Vehicle* vehicle) {
        VehicleType type = vehicle->getType();
        
        // Search all floors for available spot
        for (ParkingFloor* floor : floors) {
            ParkingSpot* spot = floor->findAvailableSpot(type);
            
            if (spot != nullptr) {
                // Found available spot!
                spot->parkVehicle(vehicle);
                
                // Generate unique ticket ID
                std::string ticketId = generateTicketId();
                
                // Create ticket
                Ticket* ticket = new Ticket(ticketId, vehicle, spot);
                
                // Store ticket for later lookup
                activeTickets[ticketId] = ticket;
                
                return ticket;
            }
        }
        
        // No available spots found
        return nullptr;
    }
    
    /**
     * Unpark a vehicle and calculate fee
     * 
     * Flow:
     * 1. Find ticket by ID
     * 2. If valid:
     *    - Get parking spot from ticket
     *    - Get parking duration
     *    - Calculate fee using pricing strategy
     *    - Free up the spot
     *    - Remove ticket from active tickets
     *    - Delete ticket (free memory)
     *    - Return fee
     * 3. If invalid:
     *    - Return -1 (error indicator)
     * 
     * Time Complexity: O(1) for ticket lookup (using map)
     * 
     * Why return -1 for error?
     * - Simple error handling for beginners
     * - Better approach: throw exception or return optional<double>
     */
    double unparkVehicle(const std::string& ticketId) {
        // Check if ticket exists
        auto it = activeTickets.find(ticketId);
        if (it == activeTickets.end()) {
            return -1.0;  // Invalid ticket
        }
        
        Ticket* ticket = it->second;
        
        // Get parking information
        ParkingSpot* spot = ticket->getSpot();
        Vehicle* vehicle = ticket->getVehicle();
        double duration = ticket->getDurationInHours();
        
        // Calculate fee using pricing strategy
        double fee = pricingStrategy->calculatePrice(vehicle->getType(), duration);
        
        // Free up the parking spot
        spot->unparkVehicle();
        
        // Remove ticket from active tickets
        activeTickets.erase(it);
        
        // Clean up ticket memory
        delete ticket;
        
        return fee;
    }
    
    /**
     * Get available spot count for vehicle type
     * 
     * Use Case:
     * - Display to users before entering
     * - Monitoring system capacity
     * 
     * Returns: Total available spots across all floors
     */
    int getAvailableSpots(VehicleType vehicleType) const {
        int total = 0;
        for (const auto& floor : floors) {
            total += floor->getAvailableSpots(vehicleType);
        }
        return total;
    }
    
    /**
     * Display parking lot status
     * 
     * Use Case:
     * - Admin dashboard
     * - Debugging
     * - User information display
     * 
     * Shows:
     * - Floor-wise availability
     * - Spot details (number, type, status)
     */
    void displayStatus() const {
        std::cout << "\n=== PARKING LOT STATUS ===\n" << std::endl;
        
        for (const auto& floor : floors) {
            std::cout << "Floor " << floor->getFloorNumber() << ":" << std::endl;
            std::cout << "  Total Spots: " << floor->getTotalSpots() << std::endl;
            std::cout << "  Available - Bikes: " << floor->getAvailableSpots(VehicleType::BIKE)
                     << " | Cars: " << floor->getAvailableSpots(VehicleType::CAR)
                     << " | Trucks: " << floor->getAvailableSpots(VehicleType::TRUCK) << std::endl;
            std::cout << std::endl;
        }
        
        std::cout << "Active Tickets: " << activeTickets.size() << "\n" << std::endl;
    }

private:
    /**
     * Generate unique ticket ID
     * 
     * Format: TICKET-0001, TICKET-0002, etc.
     * 
     * Thread Safety Note:
     * - Not thread-safe in current implementation
     * - For multithreading: add mutex around ticketCounter
     */
    std::string generateTicketId() {
        std::stringstream ss;
        ss << "TICKET-" << std::setw(4) << std::setfill('0') << ticketCounter++;
        return ss.str();
    }
};

#endif // PARKING_LOT_SERVICE_H
