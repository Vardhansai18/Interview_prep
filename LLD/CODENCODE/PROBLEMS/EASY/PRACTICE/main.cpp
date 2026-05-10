#include <iostream>
#include <vector>
#include <string>
#include <ctime>

using namespace std;

//////////////////////////////////////////////////////////////
// VEHICLE TYPE ENUM
//////////////////////////////////////////////////////////////

enum class VehicleType {
    BIKE,
    CAR,
    TRUCK
};

//////////////////////////////////////////////////////////////
// VEHICLE CLASS
//////////////////////////////////////////////////////////////

class Vehicle {
protected:
    string vehicleNumber;
    VehicleType vehicleType;

public:
    Vehicle(string number, VehicleType type)
        : vehicleNumber(number), vehicleType(type) {}

    string getVehicleNumber() {
        return vehicleNumber;
    }

    VehicleType getVehicleType() {
        return vehicleType;
    }
};

//////////////////////////////////////////////////////////////
// PARKING SPOT
//////////////////////////////////////////////////////////////

class ParkingSpot {
private:
    int id;
    VehicleType supportedType;
    Vehicle* parkedVehicle;

public:
    ParkingSpot(int id, VehicleType type)
        : id(id), supportedType(type), parkedVehicle(nullptr) {}

    bool isAvailable() {
        return parkedVehicle == nullptr;
    }

    bool parkVehicle(Vehicle* vehicle) {

        if (!isAvailable()) {
            return false;
        }

        if (vehicle->getVehicleType() != supportedType) {
            return false;
        }

        parkedVehicle = vehicle;
        return true;
    }

    void removeVehicle() {
        parkedVehicle = nullptr;
    }

    int getId() {
        return id;
    }

    VehicleType getSupportedType() {
        return supportedType;
    }
};

//////////////////////////////////////////////////////////////
// PARKING FLOOR
//////////////////////////////////////////////////////////////

class ParkingFloor {
private:
    string floorId;
    vector<ParkingSpot*> parkingSpots;

public:
    ParkingFloor(string id)
        : floorId(id) {}

    void addSpot(ParkingSpot* spot) {
        parkingSpots.push_back(spot);
    }

    ParkingSpot* findAvailableSpot(VehicleType type) {

        for (ParkingSpot* spot : parkingSpots) {

            if (spot->isAvailable() &&
                spot->getSupportedType() == type) {

                return spot;
            }
        }

        return nullptr;
    }

    string getFloorId() {
        return floorId;
    }
};

//////////////////////////////////////////////////////////////
// TICKET
//////////////////////////////////////////////////////////////

class Ticket {
private:
    string ticketId;
    time_t entryTime;
    time_t exitTime;
    double charges;

public:
    Vehicle* vehicle;
    ParkingSpot* parkingSpot;

    Ticket(string id, Vehicle* vehicle, ParkingSpot* spot)
        : ticketId(id),
          vehicle(vehicle),
          parkingSpot(spot),
          charges(0) {

        entryTime = time(nullptr);
    }

    void closeTicket(double amount) {
        charges = amount;
        exitTime = time(nullptr);
    }

    time_t getEntryTime() {
        return entryTime;
    }

    double getCharges() {
        return charges;
    }

    string getTicketId() {
        return ticketId;
    }
};

//////////////////////////////////////////////////////////////
// PRICING STRATEGY
//////////////////////////////////////////////////////////////

class PricingStrategy {
public:
    virtual double calculatePrice(Ticket* ticket) = 0;
};

//////////////////////////////////////////////////////////////
// HOURLY PRICING
//////////////////////////////////////////////////////////////

class HourlyPricingStrategy : public PricingStrategy {
private:
    double ratePerHour;

public:
    HourlyPricingStrategy(double rate)
        : ratePerHour(rate) {}

    double calculatePrice(Ticket* ticket) override {

        time_t currentTime = time(nullptr);

        double hours =
            difftime(currentTime,
                     ticket->getEntryTime()) / 3600.0;

        if (hours < 1) {
            hours = 1;
        }

        return hours * ratePerHour;
    }
};

//////////////////////////////////////////////////////////////
// PARKING LOT SERVICE
//////////////////////////////////////////////////////////////

class ParkingLotService {
private:
    vector<ParkingFloor*> parkingFloors;
    vector<Ticket*> activeTickets;

    PricingStrategy* pricingStrategy;

    int ticketCounter = 1;

public:
    ParkingLotService(PricingStrategy* strategy)
        : pricingStrategy(strategy) {}

    void addFloor(ParkingFloor* floor) {
        parkingFloors.push_back(floor);
    }

    Ticket* parkVehicle(Vehicle* vehicle) {

        for (ParkingFloor* floor : parkingFloors) {

            ParkingSpot* spot =
                floor->findAvailableSpot(
                    vehicle->getVehicleType());

            if (spot != nullptr) {

                bool parked = spot->parkVehicle(vehicle);

                if (parked) {

                    string ticketId =
                        "TICKET_" + to_string(ticketCounter++);

                    Ticket* ticket =
                        new Ticket(ticketId,
                                   vehicle,
                                   spot);

                    activeTickets.push_back(ticket);

                    cout << "Vehicle Parked Successfully\n";
                    cout << "Ticket ID: "
                         << ticketId << endl;

                    return ticket;
                }
            }
        }

        cout << "Parking Full\n";
        return nullptr;
    }

    double unparkVehicle(Ticket* ticket) {

        double amount =
            pricingStrategy->calculatePrice(ticket);

        ticket->closeTicket(amount);

        ticket->parkingSpot->removeVehicle();

        cout << "Vehicle Unparked\n";
        cout << "Amount: " << amount << endl;

        return amount;
    }
};

//////////////////////////////////////////////////////////////
// MAIN FUNCTION
//////////////////////////////////////////////////////////////

int main() {

    // Pricing Strategy
    PricingStrategy* pricing =
        new HourlyPricingStrategy(50);

    // Parking Lot Service
    ParkingLotService parkingLot(pricing);

    //////////////////////////////////////////////////////////
    // CREATE FLOOR
    //////////////////////////////////////////////////////////

    ParkingFloor* floor1 =
        new ParkingFloor("Floor_1");

    //////////////////////////////////////////////////////////
    // CREATE SPOTS
    //////////////////////////////////////////////////////////

    floor1->addSpot(
        new ParkingSpot(1, VehicleType::CAR));

    floor1->addSpot(
        new ParkingSpot(2, VehicleType::BIKE));

    floor1->addSpot(
        new ParkingSpot(3, VehicleType::TRUCK));

    //////////////////////////////////////////////////////////
    // ADD FLOOR TO PARKING LOT
    //////////////////////////////////////////////////////////

    parkingLot.addFloor(floor1);

    //////////////////////////////////////////////////////////
    // CREATE VEHICLE
    //////////////////////////////////////////////////////////

    Vehicle* car =
        new Vehicle("TS09AB1234",
                    VehicleType::CAR);

    //////////////////////////////////////////////////////////
    // PARK VEHICLE
    //////////////////////////////////////////////////////////

    Ticket* ticket =
        parkingLot.parkVehicle(car);

    //////////////////////////////////////////////////////////
    // UNPARK VEHICLE
    //////////////////////////////////////////////////////////

    if (ticket != nullptr) {

        double amount =
            parkingLot.unparkVehicle(ticket);

        cout << "Final Charges: "
             << amount << endl;
    }

    return 0;
}