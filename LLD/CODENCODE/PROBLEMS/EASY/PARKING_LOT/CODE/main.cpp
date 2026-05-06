#include <iostream>
#include <vector>
#include <memory>
#include "ParkingLotApplication.h"
#include "domain/parking/ParkingFloor.h"
#include "domain/parking/ParkingSpot.h"
#include "domain/vehicle/Bike.h"
#include "domain/vehicle/Car.h"
#include "domain/vehicle/VehicleType.h"
#include "services/ParkingLotService.h"
#include "strategy/HourlyPricingStrategy.h"

using namespace parkinglot;
using namespace parkinglot::domain::parking;
using namespace parkinglot::domain::vehicle;
using namespace parkinglot::services;
using namespace parkinglot::strategy;

int main() {
    std::cout << "=== Parking Lot System Demo ===" << std::endl << std::endl;
    
    // Create parking spots for Ground Floor - CAR
    auto spot1 = std::make_shared<ParkingSpot>("00-S1", VehicleType::CAR);
    
    // Create parking spots for 1st Floor - BIKE
    auto spot2 = std::make_shared<ParkingSpot>("01-S2", VehicleType::BIKE);
    
    // Create floors
    auto groundFloor = std::make_shared<ParkingFloor>("Ground", 
        std::vector<std::shared_ptr<ParkingSpot>>{spot1});
    auto firstFloor = std::make_shared<ParkingFloor>("First", 
        std::vector<std::shared_ptr<ParkingSpot>>{spot2});
    
    // Create pricing strategy (20 per hour)
    auto strategy = std::make_shared<HourlyPricingStrategy>(20.0);
    
    // Create parking lot service
    auto service = std::make_shared<ParkingLotService>(
        std::vector<std::shared_ptr<ParkingFloor>>{groundFloor, firstFloor},
        strategy
    );
    
    // Create parking lot application
    ParkingLotApplication application(service);
    
    // Create vehicles to park
    auto bike = std::make_shared<Bike>("ABC01");
    auto car = std::make_shared<Car>("ABC02");
    
    try {
        // Park bike
        std::cout << "Parking bike with number: " << bike->getVehicleNumber() << std::endl;
        auto bikeTicket = application.parkVehicle(bike);
        std::cout << "Bike parked at spot: " << bikeTicket->getSpot()->getId() << std::endl;
        std::cout << "Ticket ID: " << bikeTicket->getTicketId() << std::endl << std::endl;
        
        // Park car
        std::cout << "Parking car with number: " << car->getVehicleNumber() << std::endl;
        auto carTicket = application.parkVehicle(car);
        std::cout << "Car parked at spot: " << carTicket->getSpot()->getId() << std::endl;
        std::cout << "Ticket ID: " << carTicket->getTicketId() << std::endl << std::endl;
        
        // Simulate some parking time (optional - in real scenario time would pass)
        std::cout << "--- Vehicles are parked ---" << std::endl << std::endl;
        
        // Unpark vehicles
        std::cout << "Unparking bike..." << std::endl;
        double bikeFare = application.unparkVehicle(bikeTicket);
        std::cout << "Bike fare: $" << bikeFare << std::endl << std::endl;
        
        std::cout << "Unparking car..." << std::endl;
        double carFare = application.unparkVehicle(carTicket);
        std::cout << "Car fare: $" << carFare << std::endl << std::endl;
        
        std::cout << "=== Demo completed successfully ===" << std::endl;
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}
