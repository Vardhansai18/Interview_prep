#ifndef NOTIFICATION_H
#define NOTIFICATION_H

#include <string>

class Notification {
private:
    std::string userId;
    std::string message;

public:
    Notification(const std::string& userId, const std::string& message)
        : userId(userId), message(message) {}

    std::string getUserId() const {
        return userId;
    }

    std::string getMessage() const {
        return message;
    }
};

#endif // NOTIFICATION_H
