#include <vector>
#include <memory>
#include <mutex>

namespace libs
{
    using std::vector;
    using std::shared_ptr;
    using std::make_unique;
    using std::mutex;
    using std::lock_guard;

    namespace STLext
    {
        template <typename T>
        class vectorNull
        {
            vector<T> values; // use restrict keyword
            vector<unsigned char> nulls;

            // use optional to data in and out
            // or use copy
            // or use pointer
            // use release to release last N data
        };

        template <typename T>
        class TaskQueue{

            using stack_ptr = shared_ptr<vector<T>>;

            stack_ptr stack;

            stack_ptr steal(){
                auto temp = std::move(stack);
                stack = make_unique<vector<T>>();
                return temp;
            };
            
            public:
            void push(T t){stack->push_back(t);};
        };

        template <typename T>
        class taskQueueSafe :public TaskQueue<T>{

            mutex m;
            using stack_ptr = shared_ptr<vector<T>>;

            stack_ptr steal() override {
                lock_guard<mutex> lg{m};
                //pode ser try lock aqui talvez
                return TaskQueueBase<T>::steal();
            };
            
            public:
            void push(T t) override {
                lock_guard<mutex> lg{m};
                TaskQueueBase<T>::push(t);
            };
        };

        class chain;

        eastl
        class intrusive_list + direct access;
    }
}