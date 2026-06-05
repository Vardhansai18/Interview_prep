#include <iostream>
#include <chrono>
#include <thread>
#include <ctime>

using namespace std;

class TokenBucket
{
private:
    double tokens;
    int capacity;
    double refillRate; // tokens per second
    long long lastRefillTime;

    long long getCurrentTime()
    {
        return chrono::duration_cast<chrono::seconds>(
                   chrono::system_clock::now().time_since_epoch())
            .count();
    }

    void refill()
    {
        long long currentTime = getCurrentTime();

        long long elapsedTime =
            currentTime - lastRefillTime;

        cout << "\n----- Refill Started -----\n";

        time_t now = time(nullptr);
        cout << "Current Time    : "
             << ctime(&now);

        cout << "Elapsed Time    : "
             << elapsedTime
             << " sec\n";

        cout << "Tokens Before   : "
             << tokens
             << endl;

        tokens += elapsedTime * refillRate;

        if (tokens > capacity)
        {
            tokens = capacity;
        }

        cout << "Tokens After    : "
             << tokens
             << endl;

        lastRefillTime = currentTime;

        cout << "--------------------------\n";
    }

public:
    TokenBucket(
        int cap,
        double rate)
    {
        capacity = cap;
        refillRate = rate;
        tokens = capacity;
        lastRefillTime = getCurrentTime();
    }

    bool allowRequest()
    {
        refill();

        if (tokens < 1)
        {
            cout << "Request Rejected ❌\n";
            return false;
        }

        tokens--;

        cout << "Request Allowed ✅\n";
        cout << "Remaining Tokens : "
             << tokens
             << endl;

        return true;
    }
};

int main()
{
    TokenBucket bucket(
        5, // capacity
        1  // refill rate = 1 token/sec
    );

    cout << "\n=== Token Bucket Simulation ===\n";

    for (int i = 1; i <= 10; i++)
    {
        cout << "\n===== Request "
             << i
             << " =====\n";

        bucket.allowRequest();

        this_thread::sleep_for(
            chrono::seconds(2));
    }

    return 0;
}