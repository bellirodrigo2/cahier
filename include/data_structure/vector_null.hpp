#ifndef _VECTOR_NULL_HPP_
#define _VECTOR_NULL_HPP_

#include <vector>

namespace task_queue
{
    using std::vector;

    template <typename T>
    class vector_null :public vector<T>{};
}

#endif