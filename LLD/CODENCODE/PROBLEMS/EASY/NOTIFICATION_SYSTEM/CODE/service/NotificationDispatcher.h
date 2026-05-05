#ifndef NOTIFICATIONDISPATCHER_H
#define NOTIFICATIONDISPATCHER_H

#include <memory>
#include "UserPreferenceService.h"
#include "../factory/NotificationChannelFactory.h"
#include "../model/Notification.h"

class NotificationDispatcher {
private:
    std::shared_ptr<UserPreferenceService> preferenceService;

public:
    NotificationDispatcher(std::shared_ptr<UserPreferenceService> preferenceService)
        : preferenceService(preferenceService) {}

    void dispatch(const Notification& notification) {
        UserPreference preference = 
            preferenceService->getPreference(notification.getUserId());

        std::set<ChannelType> channels = preference.getPreferredChannels();

        for (const auto& channelType : channels) {
            auto channel = NotificationChannelFactory::getChannel(channelType);
            if (channel) {
                channel->send(notification);
            }
        }
    }
};

#endif // NOTIFICATIONDISPATCHER_H
