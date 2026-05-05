#ifndef ASYNCNOTIFICATIONSERVICE_H
#define ASYNCNOTIFICATIONSERVICE_H

#include <memory>
#include <thread>
#include <vector>
#include <queue>
#include <mutex>
#include <condition_variable>
#include <functional>
#include "../service/NotificationDispatcher.h"
#include "../model/Notification.h"

class AsyncNotificationService {
private:
    std::shared_ptr<NotificationDispatcher> dispatcher;
    std::vector<std::thread> workers;
    std::queue<std::function<void()>> tasks;
    std::mutex queueMutex;
    std::condition_variable condition;
    bool stop;

    void workerThread() {
        while (true) {
            std::function<void()> task;
            {
                std::unique_lock<std::mutex> lock(queueMutex);
                condition.wait(lock, [this] { return stop || !tasks.empty(); });
                
                if (stop && tasks.empty()) {
                    return;
                }
                
                task = std::move(tasks.front());
                tasks.pop();
            }
            task();
        }
    }

public:
    AsyncNotificationService(std::shared_ptr<NotificationDispatcher> dispatcher, size_t threadCount = 10)
        : dispatcher(dispatcher), stop(false) {
        for (size_t i = 0; i < threadCount; ++i) {
            workers.emplace_back([this] { workerThread(); });
        }
    }

    ~AsyncNotificationService() {
        {
            std::unique_lock<std::mutex> lock(queueMutex);
            stop = true;
        }
        condition.notify_all();
        for (auto& worker : workers) {
            if (worker.joinable()) {
                worker.join();
            }
        }
    }

    void sendNotification(const Notification& notification) {
        {
            std::unique_lock<std::mutex> lock(queueMutex);
            tasks.emplace([this, notification] {
                dispatcher->dispatch(notification);
            });
        }
        condition.notify_one();
    }
};

#endif // ASYNCNOTIFICATIONSERVICE_H
