#ifndef _CAH_TYPES_HPP
#define _CAH_TYPES_HPP

#include <chrono>

namespace cahier{
    using clock = std::chrono::steady_clock;
    using time_duration = std::chrono::milliseconds;
    using time_point = std::chrono::time_point<clock>;
}

#endif