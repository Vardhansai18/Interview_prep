#ifndef NOTIFICATIONCHANNEL_H
#define NOTIFICATIONCHANNEL_H

#include "../model/Notification.h"

class NotificationChannel {
public:
    virtual ~NotificationChannel() = default;
    virtual void send(const Notification& notification) = 0;
};

#endif // NOTIFICATIONCHANNEL_H
