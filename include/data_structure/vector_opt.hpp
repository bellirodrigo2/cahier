#ifndef _VECTOR_NULL_HPP_
#define _VECTOR_NULL_HPP_

#include <vector>

namespace vector_ext
{
    using std::vector;

    template <typename T>
    class vector_optional :public vector<T>{};
}

#endif