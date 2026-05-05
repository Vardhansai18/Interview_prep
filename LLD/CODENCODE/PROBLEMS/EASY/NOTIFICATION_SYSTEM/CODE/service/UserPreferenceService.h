#ifndef USERPREFERENCESERVICE_H
#define USERPREFERENCESERVICE_H

#include <unordered_map>
#include <mutex>
#include <set>
#include "../model/UserPreference.h"

class UserPreferenceService {
private:
    std::unordered_map<std::string, UserPreference> preferences;
    mutable std::mutex mutex_;

public:
    void savePreference(const UserPreference& preference) {
        std::lock_guard<std::mutex> lock(mutex_);
        preferences.insert_or_assign(preference.getUserId(), preference);
    }

    UserPreference getPreference(const std::string& userId) const {
        std::lock_guard<std::mutex> lock(mutex_);
        auto it = preferences.find(userId);
        if (it != preferences.end()) {
            return it->second;
        }
        // Default preference with EMAIL channel
        return UserPreference(userId, {ChannelType::EMAIL});
    }
};

#endif // USERPREFERENCESERVICE_H
