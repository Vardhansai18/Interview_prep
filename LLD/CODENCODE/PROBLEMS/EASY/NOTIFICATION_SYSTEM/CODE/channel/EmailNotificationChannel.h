#ifndef EMAILNOTIFICATIONCHANNEL_H
#define EMAILNOTIFICATIONCHANNEL_H

#include "NotificationChannel.h"
#include <iostream>

class EmailNotificationChannel : public NotificationChannel {
public:
    void send(const Notification& notification) override {
        std::cout << "Sending EMAIL to user " << notification.getUserId()
                  << ": " << notification.getMessage() << std::endl;
    }
};

#endif // EMAILNOTIFICATIONCHANNEL_H
