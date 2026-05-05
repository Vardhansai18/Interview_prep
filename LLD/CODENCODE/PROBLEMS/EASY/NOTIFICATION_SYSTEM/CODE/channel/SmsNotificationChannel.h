#ifndef SMSNOTIFICATIONCHANNEL_H
#define SMSNOTIFICATIONCHANNEL_H

#include "NotificationChannel.h"
#include <iostream>

class SmsNotificationChannel : public NotificationChannel {
public:
    void send(const Notification& notification) override {
        std::cout << "Sending SMS to user " << notification.getUserId()
                  << ": " << notification.getMessage() << std::endl;
    }
};

#endif // SMSNOTIFICATIONCHANNEL_H
