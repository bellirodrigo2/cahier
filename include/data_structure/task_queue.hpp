#ifndef _TASK_QUEUE_HPP_
#define _TASK_QUEUE_HPP_

namespace task_queue
{
    template <typename T>
    class TaskQueue
    {
        using stack_ptr = shared_ptr<vector<T>>;

        stack_ptr stack;

        stack_ptr steal()
        {
            auto temp = std::move(stack);
            stack = make_unique<vector<T>>();
            return temp;
        };

    public:
        void push(T t) { stack->push_back(t); };
    };

    template <typename T>
    class taskQueueSafe : public TaskQueue<T>
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