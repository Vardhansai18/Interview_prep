#include "ParkingException.h"

namespace parkinglot {
namespace exception {

ParkingException::ParkingException(const std::string& message)
    : message(message) {}

const char* ParkingException::what() const noexcept {
    return message.c_str();
}

} // namespace exception
} // namespace parkinglot
