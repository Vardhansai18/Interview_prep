#ifndef PUSHNOTIFICATIONCHANNEL_H
#define PUSHNOTIFICATIONCHANNEL_H

#include "NotificationChannel.h"
#include <iostream>

class PushNotificationChannel : public NotificationChannel {
public:
    void send(const Notification& notification) override {
        std::cout << "Sending PUSH to user " << notification.getUserId()
                  << ": " << notification.getMessage() << std::endl;
    }
};

#endif // PUSHNOTIFICATIONCHANNEL_H
