#include <iostream>
#include <iomanip>
#include <thread>
#include <chrono>
#include "src/models/Vehicle.h"
#include "src/models/Car.h"
#include "src/models/Bike.h"
#include "src/models/Truck.h"
#include "src/models/ParkingSpot.h"
#include "src/models/ParkingFloor.h"
#include "src/models/Ticket.h"
#include "src/strategies/SimplePricingStrategy.h"
#include "src/services/ParkingLotService.h"

/**
 * PARKING LOT SYSTEM - DEMO APPLICATION
 * 
 * Purpose: Demonstrate complete parking lot system
 * 
 * This demo shows:
 * 1. How to initialize parking lot structure
 * 2. How to park vehicles
 * 3. How to unpark vehicles and calculate fees
 * 4. How the system handles "lot full" scenario
 * 5. Real-world usage patterns
 * 
 * Learning Objectives:
 * - See SOLID principles in action
 * - Understand object interactions
 * - Learn typical system flows
 */

// Helper function to print section headers
void printSection(const std::string& title) {
    std::cout << "\n" << std::string(60, '=') << std::endl;
    std::cout << "  " << title << std::endl;
    std::cout << std::string(60, '=') << "\n" << std::endl;
}

// Helper function to simulate time passing (for demo purposes)
void simulateTimePassing(int seconds) {
    std::cout << "⏰ Simulating " << seconds << " seconds passing..." << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(seconds));
}

int main() {
    std::cout << "\n";
    std::cout << "╔══════════════════════════════════════════════════════════╗\n";
    std::cout << "║     PARKING LOT SYSTEM - BEGINNER FRIENDLY DEMO          ║\n";
    std::cout << "║                                                          ║\n";
    std::cout << "║  Demonstrating SOLID Principles in Action               ║\n";
    std::cout << "╚══════════════════════════════════════════════════════════╝\n";
    
    // ========================================================================
    // STEP 1: Initialize the Parking Lot
    // ========================================================================
    printSection("STEP 1: Initialize Parking Lot Structure");
    
    std::cout << "Creating pricing strategy (SimplePricingStrategy)..." << std::endl;
    PricingStrategy* pricingStrategy = new SimplePricingStrategy();
    
    std::cout << "Creating parking lot service..." << std::endl;
    ParkingLotService parkingLot(pricingStrategy);
    
    // Create Floor 0 (Ground Floor)
    std::cout << "\nSetting up Floor 0 (Ground Floor):" << std::endl;
    ParkingFloor* floor0 = new ParkingFloor(0);
    
    // Add 2 bike spots
    floor0->addSpot(new ParkingSpot(1, VehicleType::BIKE));
    floor0->addSpot(new ParkingSpot(2, VehicleType::BIKE));
    std::cout << "  ✓ Added 2 Bike spots (B1, B2)" << std::endl;
    
    // Add 2 car spots
    floor0->addSpot(new ParkingSpot(3, VehicleType::CAR));
    floor0->addSpot(new ParkingSpot(4, VehicleType::CAR));
    std::cout << "  ✓ Added 2 Car spots (C3, C4)" << std::endl;
    
    // Add 1 truck spot
    floor0->addSpot(new ParkingSpot(5, VehicleType::TRUCK));
    std::cout << "  ✓ Added 1 Truck spot (T5)" << std::endl;
    
    parkingLot.addFloor(floor0);
    
    // Create Floor 1 (First Floor)
    std::cout << "\nSetting up Floor 1 (First Floor):" << std::endl;
    ParkingFloor* floor1 = new ParkingFloor(1);
    
    // Add 1 bike spot, 2 car spots
    floor1->addSpot(new ParkingSpot(6, VehicleType::BIKE));
    floor1->addSpot(new ParkingSpot(7, VehicleType::CAR));
    floor1->addSpot(new ParkingSpot(8, VehicleType::CAR));
    std::cout << "  ✓ Added 1 Bike spot (B6)" << std::endl;
    std::cout << "  ✓ Added 2 Car spots (C7, C8)" << std::endl;
    
    parkingLot.addFloor(floor1);
    
    std::cout << "\n✅ Parking Lot initialized successfully!" << std::endl;
    
    // Display initial status
    parkingLot.displayStatus();
    
    // ========================================================================
    // STEP 2: Park Vehicles (Successful Cases)
    // ========================================================================
    printSection("STEP 2: Park Vehicles");
    
    // Create vehicles
    std::cout << "Creating vehicles..." << std::endl;
    Vehicle* bike1 = new Bike("BIKE-001");
    Vehicle* car1 = new Car("CAR-ABC-123");
    Vehicle* truck1 = new Truck("TRUCK-XYZ-789");
    Vehicle* car2 = new Car("CAR-DEF-456");
    std::cout << "  ✓ Created: 1 Bike, 2 Cars, 1 Truck\n" << std::endl;
    
    // Park Bike
    std::cout << "🏍️  Parking Bike (BIKE-001)..." << std::endl;
    Ticket* ticket1 = parkingLot.parkVehicle(bike1);
    if (ticket1) {
        std::cout << "  ✅ SUCCESS! Ticket ID: " << ticket1->getTicketId() << std::endl;
        std::cout << "     Entry Time: " << ticket1->getFormattedEntryTime();
    }
    
    simulateTimePassing(1);  // Simulate 1 second gap
    
    // Park Car 1
    std::cout << "\n🚗 Parking Car (CAR-ABC-123)..." << std::endl;
    Ticket* ticket2 = parkingLot.parkVehicle(car1);
    if (ticket2) {
        std::cout << "  ✅ SUCCESS! Ticket ID: " << ticket2->getTicketId() << std::endl;
        std::cout << "     Entry Time: " << ticket2->getFormattedEntryTime();
    }
    
    simulateTimePassing(1);
    
    // Park Truck
    std::cout << "\n🚚 Parking Truck (TRUCK-XYZ-789)..." << std::endl;
    Ticket* ticket3 = parkingLot.parkVehicle(truck1);
    if (ticket3) {
        std::cout << "  ✅ SUCCESS! Ticket ID: " << ticket3->getTicketId() << std::endl;
        std::cout << "     Entry Time: " << ticket3->getFormattedEntryTime();
    }
    
    simulateTimePassing(1);
    
    // Park Car 2
    std::cout << "\n🚗 Parking Car (CAR-DEF-456)..." << std::endl;
    Ticket* ticket4 = parkingLot.parkVehicle(car2);
    if (ticket4) {
        std::cout << "  ✅ SUCCESS! Ticket ID: " << ticket4->getTicketId() << std::endl;
        std::cout << "     Entry Time: " << ticket4->getFormattedEntryTime();
    }
    
    // Display status after parking
    parkingLot.displayStatus();
    
    // ========================================================================
    // STEP 3: Try Parking When Spots Are Full
    // ========================================================================
    printSection("STEP 3: Handle Parking Lot Full Scenario");
    
    std::cout << "Attempting to park more cars than available spots...\n" << std::endl;
    
    Vehicle* car3 = new Car("CAR-FULL-999");
    std::cout << "🚗 Trying to park Car (CAR-FULL-999)..." << std::endl;
    Ticket* ticket5 = parkingLot.parkVehicle(car3);
    
    if (ticket5) {
        std::cout << "  ✅ Parked successfully" << std::endl;
    } else {
        std::cout << "  ❌ PARKING LOT FULL! No available spots for CAR." << std::endl;
        std::cout << "     System correctly handled the overflow scenario." << std::endl;
        delete car3;  // Clean up vehicle since it wasn't parked
    }
    
    // ========================================================================
    // STEP 4: Unpark Vehicles and Calculate Fees
    // ========================================================================
    printSection("STEP 4: Unpark Vehicles and Calculate Fees");
    
    std::cout << "Simulating time passing (3 seconds = represents 3+ hours for demo)...\n" << std::endl;
    simulateTimePassing(3);
    
    // Unpark Bike
    std::cout << "🏍️  Unparking Bike (Ticket: " << ticket1->getTicketId() << ")..." << std::endl;
    double fee1 = parkingLot.unparkVehicle(ticket1->getTicketId());
    if (fee1 >= 0) {
        std::cout << "  ✅ Bike unparked successfully" << std::endl;
        std::cout << "     💰 Fee: $" << std::fixed << std::setprecision(2) << fee1 << std::endl;
        std::cout << "     (Bike rate: $2/hour, Duration: " << ticket1->getDurationInHours() << " hours)" << std::endl;
    }
    
    std::cout << std::endl;
    
    // Unpark Car 1
    std::cout << "🚗 Unparking Car (Ticket: " << ticket2->getTicketId() << ")..." << std::endl;
    double fee2 = parkingLot.unparkVehicle(ticket2->getTicketId());
    if (fee2 >= 0) {
        std::cout << "  ✅ Car unparked successfully" << std::endl;
        std::cout << "     💰 Fee: $" << std::fixed << std::setprecision(2) << fee2 << std::endl;
        std::cout << "     (Car rate: $5/hour)" << std::endl;
    }
    
    std::cout << std::endl;
    
    // Unpark Truck
    std::cout << "🚚 Unparking Truck (Ticket: " << ticket3->getTicketId() << ")..." << std::endl;
    double fee3 = parkingLot.unparkVehicle(ticket3->getTicketId());
    if (fee3 >= 0) {
        std::cout << "  ✅ Truck unparked successfully" << std::endl;
        std::cout << "     💰 Fee: $" << std::fixed << std::setprecision(2) << fee3 << std::endl;
        std::cout << "     (Truck rate: $10/hour)" << std::endl;
    }
    
    // Display final status
    parkingLot.displayStatus();
    
    // ========================================================================
    // STEP 5: Test Invalid Ticket
    // ========================================================================
    printSection("STEP 5: Handle Invalid Ticket Scenario");
    
    std::cout << "Attempting to unpark with invalid ticket...\n" << std::endl;
    std::cout << "❌ Trying ticket: INVALID-9999" << std::endl;
    double invalidFee = parkingLot.unparkVehicle("INVALID-9999");
    
    if (invalidFee < 0) {
        std::cout << "  ✅ System correctly rejected invalid ticket" << std::endl;
        std::cout << "     Returned error code: " << invalidFee << std::endl;
    }
    
    // ========================================================================
    // STEP 6: Summary and Key Takeaways
    // ========================================================================
    printSection("SUMMARY & KEY TAKEAWAYS");
    
    std::cout << "✅ All core functionalities demonstrated:\n" << std::endl;
    std::cout << "   1. ✓ Park vehicles (different types)" << std::endl;
    std::cout << "   2. ✓ Unpark vehicles and calculate fees" << std::endl;
    std::cout << "   3. ✓ Handle parking lot full scenario" << std::endl;
    std::cout << "   4. ✓ Handle invalid ticket scenario" << std::endl;
    std::cout << "   5. ✓ Display lot status" << std::endl;
    
    std::cout << "\n📚 SOLID Principles Demonstrated:\n" << std::endl;
    std::cout << "   S - Single Responsibility: Each class has one clear job" << std::endl;
    std::cout << "   O - Open/Closed: Easy to add new vehicle types/pricing" << std::endl;
    std::cout << "   L - Liskov Substitution: Car/Bike/Truck interchangeable" << std::endl;
    std::cout << "   I - Interface Segregation: Focused PricingStrategy interface" << std::endl;
    std::cout << "   D - Dependency Inversion: Service depends on abstractions" << std::endl;
    
    std::cout << "\n🎯 Next Steps for Learning:\n" << std::endl;
    std::cout << "   1. Read MULTITHREADING_GUIDE.md for thread-safe version" << std::endl;
    std::cout << "   2. Try adding new vehicle types (e.g., Van, Bus)" << std::endl;
    std::cout << "   3. Implement different pricing strategies" << std::endl;
    std::cout << "   4. Add reservation system" << std::endl;
    std::cout << "   5. Add payment processing" << std::endl;
    
    // ========================================================================
    // Cleanup
    // ========================================================================
    std::cout << "\n🧹 Cleaning up resources..." << std::endl;
    
    // Unpark remaining vehicle
    if (ticket4) {
        parkingLot.unparkVehicle(ticket4->getTicketId());
    }
    
    // Delete vehicles
    delete bike1;
    delete car1;
    delete car2;
    delete truck1;
    
    // Delete pricing strategy
    delete pricingStrategy;
    
    // ParkingLotService destructor will clean up floors and tickets
    
    std::cout << "✅ All resources cleaned up successfully!" << std::endl;
    
    std::cout << "\n";
    std::cout << "╔══════════════════════════════════════════════════════════╗\n";
    std::cout << "║                  DEMO COMPLETED!                         ║\n";
    std::cout << "║                                                          ║\n";
    std::cout << "║  Thank you for using the Parking Lot System!            ║\n";
    std::cout << "╚══════════════════════════════════════════════════════════╝\n";
    std::cout << std::endl;
    
    return 0;
}
