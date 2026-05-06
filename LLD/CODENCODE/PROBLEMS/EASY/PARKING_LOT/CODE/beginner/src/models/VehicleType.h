#ifndef VEHICLE_TYPE_H
#define VEHICLE_TYPE_H

/**
 * VehicleType Enum
 * 
 * Purpose: Define all types of vehicles that can park
 * 
 * SOLID Principle: Single Responsibility
 * - This enum has one job: distinguish vehicle types
 * 
 * Why enum?
 * - Type safety: Can't assign invalid types
 * - Clear intent: Makes code self-documenting
 * - Easy to extend: Add new types as needed
 */

enum class VehicleType {
    BIKE,   // Small vehicle - takes 1 spot
    CAR,    // Medium vehicle - takes 1 spot
    TRUCK   // Large vehicle - takes 1 spot (can be extended to take more)
};

#endif // VEHICLE_TYPE_H
