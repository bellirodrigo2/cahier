#ifndef _TASK_QUEUE_HPP_
#define _TASK_QUEUE_HPP_

#include <memory>
#include <vector>

namespace task_queue
{
    using std::vector;

    template <typename T, typename Q = vector<T>>
    class task_queue
    {
        using s_ptr std::shared_ptr<T>;

        Q stack;

        Q steal()
        {
            auto temp = std::move(stack);
            stack = make_unique<Q>();
            return temp;
        };

    public:
        void push(T t) { stack->push_back(t); };
    };

    template <typename T>                        //K deveria ser um unnamed hash map
    class task_queue_ext : public task_queue<T, hash_map<K,T>>{

        public:

        void aggregate(K key, T val); // agregate data to existing task
        void update(K key, T val); // update data on existing task

    };

    template <typename T>
    class taskQueueSafe : public task_queue<T>
    {

        mutex m;
        using stack_ptr = shared_ptr<vector<T>>;

        stack_ptr steal() override
        {
            lock_guard<mutex> lg{m};
            // pode ser try lock aqui talvez
            return TaskQueueBase<T>::steal();
        };

    public:
        void push(T t) override
        {
            lock_guard<mutex> lg{m};
            TaskQueueBase<T>::push(t);
        };
    };

}

#endif