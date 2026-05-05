# Notification System - C++ Implementation

## Overview
This is a C++ implementation of a notification system that demonstrates Low-Level Design (LLD) principles including SOLID principles, design patterns, and thread safety.

## Architecture

### Design Patterns Used
1. **Factory Pattern**: `NotificationChannelFactory` creates notification channel instances
2. **Strategy Pattern**: Different notification channels implement the same interface
3. **Thread Pool Pattern**: `AsyncNotificationService` implements an asynchronous thread pool

### SOLID Principles
- **Single Responsibility Principle (SRP)**: Each class has one clear responsibility
- **Open/Closed Principle (OCP)**: New channels can be added without modifying existing code
- **Liskov Substitution Principle (LSP)**: All channels are interchangeable through the base interface
- **Interface Segregation Principle (ISP)**: Interfaces are focused and minimal
- **Dependency Inversion Principle (DIP)**: High-level modules depend on abstractions

## Project Structure

```
CODE/
├── model/
│   ├── ChannelType.h          # Enum for channel types
│   ├── Notification.h         # Notification data model
│   └── UserPreference.h       # User preference data model
├── channel/
│   ├── NotificationChannel.h  # Abstract interface
│   ├── EmailNotificationChannel.h
│   ├── SmsNotificationChannel.h
│   └── PushNotificationChannel.h
├── factory/
│   └── NotificationChannelFactory.h  # Factory for channels
├── service/
│   ├── UserPreferenceService.h      # Manages user preferences
│   └── NotificationDispatcher.h     # Dispatches notifications
├── api/
│   ├── NotificationService.h        # Synchronous API
│   └── AsyncNotificationService.h   # Asynchronous API
├── Main.cpp                           # Demo application
├── Makefile                          # Build configuration
└── README.md                         # This file
```

## Components

### 1. Model Layer
- **ChannelType**: Enum defining EMAIL, SMS, and PUSH channels
- **Notification**: Contains userId and message
- **UserPreference**: Maps users to their preferred notification channels

### 2. Channel Layer
- **NotificationChannel**: Abstract interface for all channels
- **EmailNotificationChannel**: Sends email notifications
- **SmsNotificationChannel**: Sends SMS notifications
- **PushNotificationChannel**: Sends push notifications

### 3. Factory Layer
- **NotificationChannelFactory**: Creates appropriate channel instances based on type

### 4. Service Layer
- **UserPreferenceService**: Thread-safe storage and retrieval of user preferences
- **NotificationDispatcher**: Dispatches notifications to preferred channels

### 5. API Layer
- **NotificationService**: Synchronous notification sending
- **AsyncNotificationService**: Asynchronous notification sending with thread pool

## Thread Safety
- **UserPreferenceService**: Uses `std::mutex` for thread-safe access to preferences
- **AsyncNotificationService**: Implements a thread pool with condition variables for efficient async processing

## Building and Running

### Prerequisites
- C++17 compatible compiler (g++, clang++)
- Make

### Build
```bash
make
```

### Run
```bash
make run
```

### Clean
```bash
make clean
```

## Usage Example

```cpp
// Create preference service
auto preferenceService = std::make_shared<UserPreferenceService>();

// Set user preferences
preferenceService->savePreference(
    UserPreference("user123", {ChannelType::EMAIL, ChannelType::SMS})
);

// Create dispatcher
auto dispatcher = std::make_shared<NotificationDispatcher>(preferenceService);

// Create services
NotificationService syncService(dispatcher);
AsyncNotificationService asyncService(dispatcher);

// Send notification
Notification notification("user123", "Your order has been shipped!");
syncService.sendNotification(notification);
asyncService.sendNotification(notification);
```

## Extending the System

### Adding a New Channel
1. Create a new class inheriting from `NotificationChannel`
2. Implement the `send()` method
3. Add the channel type to `ChannelType` enum
4. Update `NotificationChannelFactory` to create the new channel

Example:
```cpp
class WhatsAppNotificationChannel : public NotificationChannel {
public:
    void send(const Notification& notification) override {
        std::cout << "Sending WhatsApp to user " << notification.getUserId()
                  << ": " << notification.getMessage() << std::endl;
    }
};
```

## Key Features
- ✅ Multiple notification channels (EMAIL, SMS, PUSH)
- ✅ User preference management
- ✅ Synchronous and asynchronous notification sending
- ✅ Thread-safe operations
- ✅ Factory pattern for channel creation
- ✅ Extensible architecture
- ✅ SOLID principles implementation

## Conversion Notes
This C++ implementation is converted from the original Java version with the following adaptations:
- Used `std::shared_ptr` for polymorphic objects
- Used `std::mutex` for thread safety (equivalent to Java's `ConcurrentHashMap`)
- Implemented custom thread pool (equivalent to Java's `ExecutorService`)
- Used header-only design for simplicity
- Added proper RAII and move semantics
