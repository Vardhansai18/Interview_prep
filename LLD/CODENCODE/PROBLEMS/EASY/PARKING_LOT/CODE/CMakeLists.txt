cmake_minimum_required(VERSION 3.10)
project(ParkingLotSystem VERSION 1.0)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Add compiler flags
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -pthread")

# Include directories
include_directories(${CMAKE_CURRENT_SOURCE_DIR})

# Source files
set(DOMAIN_VEHICLE_SOURCES
    domain/vehicle/Vehicle.cpp
    domain/vehicle/Car.cpp
    domain/vehicle/Bike.cpp
    domain/vehicle/Truck.cpp
)

set(DOMAIN_PARKING_SOURCES
    domain/parking/ParkingSpot.cpp
    domain/parking/ParkingFloor.cpp
)

set(DOMAIN_TICKET_SOURCES
    domain/ticket/Ticket.cpp
)

set(STRATEGY_SOURCES
    strategy/HourlyPricingStrategy.cpp
)

set(SERVICE_SOURCES
    services/ParkingLotService.cpp
)

set(EXCEPTION_SOURCES
    exception/ParkingException.cpp
)

set(APPLICATION_SOURCES
    ParkingLotApplication.cpp
)

# All source files
set(ALL_SOURCES
    ${DOMAIN_VEHICLE_SOURCES}
    ${DOMAIN_PARKING_SOURCES}
    ${DOMAIN_TICKET_SOURCES}
    ${STRATEGY_SOURCES}
    ${SERVICE_SOURCES}
    ${EXCEPTION_SOURCES}
    ${APPLICATION_SOURCES}
)

# Create executable
add_executable(parking_lot_demo main.cpp ${ALL_SOURCES})

# Link pthread library
target_link_libraries(parking_lot_demo pthread)

# Optional: Create a library
add_library(parking_lot_lib STATIC ${ALL_SOURCES})

message(STATUS "Parking Lot System configured successfully!")
