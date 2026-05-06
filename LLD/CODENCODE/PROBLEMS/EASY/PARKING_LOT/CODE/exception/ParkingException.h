#ifndef PARKING_EXCEPTION_H
#define PARKING_EXCEPTION_H

#include <exception>
#include <string>

namespace parkinglot {
namespace exception {

class ParkingException : public std::exception {
private:
    std::string message;

public:
    explicit ParkingException(const std::string& message);
    const char* what() const noexcept override;
};

} // namespace exception
} // namespace parkinglot

#endif // PARKING_EXCEPTION_H
