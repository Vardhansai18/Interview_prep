#ifndef NOTIFICATIONCHANNELFACTORY_H
#define NOTIFICATIONCHANNELFACTORY_H

#include <memory>
#include "../channel/NotificationChannel.h"
#include "../channel/EmailNotificationChannel.h"
#include "../channel/SmsNotificationChannel.h"
#include "../channel/PushNotificationChannel.h"
#include "../model/ChannelType.h"

class NotificationChannelFactory {
public:
    static std::shared_ptr<NotificationChannel> getChannel(ChannelType channelType) {
        switch (channelType) {
            case ChannelType::EMAIL:
                return std::make_shared<EmailNotificationChannel>();
            case ChannelType::SMS:
                return std::make_shared<SmsNotificationChannel>();
            case ChannelType::PUSH:
                return std::make_shared<PushNotificationChannel>();
            default:
                return nullptr;
        }
    }
};

#endif // NOTIFICATIONCHANNELFACTORY_H
