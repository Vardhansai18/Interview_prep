# Build Instructions

## Quick Start

```bash
# Create build directory
mkdir -p build && cd build

# Configure
cmake ..

# Build
make -j$(nproc)

# Run
./parking_lot_demo
```

## Clean Build

```bash
# Remove old build files
rm -rf build

# Fresh build
mkdir build && cd build
cmake ..
make
```

## Compilation Flags

The project uses:
- `-std=c++17`: C++17 standard
- `-Wall -Wextra`: All warnings enabled
- `-pthread`: POSIX threads support

## Troubleshooting

### Error: "cmake: command not found"
```bash
# Ubuntu/Debian
sudo apt-get install cmake

# Fedora/RHEL
sudo dnf install cmake
```

### Error: "No CMAKE_CXX_COMPILER could be found"
```bash
# Ubuntu/Debian
sudo apt-get install build-essential g++

# Fedora/RHEL
sudo dnf install gcc-c++
```

### Linking errors with pthread
Make sure you have pthread library:
```bash
# Usually included with build-essential on Linux
sudo apt-get install build-essential
```
