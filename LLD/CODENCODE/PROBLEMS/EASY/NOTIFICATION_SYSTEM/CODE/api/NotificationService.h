#ifndef NOTIFICATIONSERVICE_H
#define NOTIFICATIONSERVICE_H

#include <memory>
#include "../service/NotificationDispatcher.h"
#include "../model/Notification.h"

class NotificationService {
private:
    std::shared_ptr<NotificationDispatcher> dispatcher;

public:
    NotificationService(std::shared_ptr<NotificationDispatcher> dispatcher)
        : dispatcher(dispatcher) {}

    void sendNotification(const Notification& notification) {
        dispatcher->dispatch(notification);
    }
};

#endif // NOTIFICATIONSERVICE_H
