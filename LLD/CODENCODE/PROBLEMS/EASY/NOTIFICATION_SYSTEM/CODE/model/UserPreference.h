#ifndef USERPREFERENCE_H
#define USERPREFERENCE_H

#include <string>
#include <set>
#include "ChannelType.h"

class UserPreference {
private:
    std::string userId;
    std::set<ChannelType> preferredChannels;

public:
    UserPreference(const std::string& userId, const std::set<ChannelType>& preferredChannels)
        : userId(userId), preferredChannels(preferredChannels) {}

    std::string getUserId() const {
        return userId;
    }

    std::set<ChannelType> getPreferredChannels() const {
        return preferredChannels;
    }
};

#endif // USERPREFERENCE_H
