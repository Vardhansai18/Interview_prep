#include <iostream>
#include <memory>
#include <set>
#include <thread>
#include <chrono>
#include "model/ChannelType.h"
#include "model/Notification.h"
#include "model/UserPreference.h"
#include "service/UserPreferenceService.h"
#include "service/NotificationDispatcher.h"
#include "api/NotificationService.h"
#include "api/AsyncNotificationService.h"

int main() {
    // Defining preference service
    auto preferenceService = std::make_shared<UserPreferenceService>();

    // Defining user preference with Email and SMS as preferred channels
    preferenceService->savePreference(
        UserPreference("user123", {ChannelType::EMAIL, ChannelType::SMS})
    );

    // Defining notification dispatcher
    auto dispatcher = std::make_shared<NotificationDispatcher>(preferenceService);

    // Defining synchronous service
    NotificationService service(dispatcher);

    // Defining async service
    AsyncNotificationService asyncService(dispatcher);

    // Defining notification to send through multiple channels
    Notification notification("user123", "Your order has been shipped!");

    std::cout << "=== Synchronous Notification ===" << std::endl;
    // Sending notification through synchronous service
    service.sendNotification(notification);

    std::cout << "\n=== Asynchronous Notification ===" << std::endl;
    // Sending notification through asynchronous service
    asyncService.sendNotification(notification);

    // Wait a bit for async notifications to complete
    std::this_thread::sleep_for(std::chrono::milliseconds(100));

    std::cout << "\nNotification system demo completed!" << std::endl;

    return 0;
}
