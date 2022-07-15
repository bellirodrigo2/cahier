
#include <string>
#include <vector>
#include <array>
#include <algorithm>
#include <utility>
#include <chrono>
#include <thread>

namespace core
{
    using std::string;
    using std::array;
    using std::vector;
    using std::pair;
    using std::make_pair;
    using std::for_each;

    using acum = long;
    using keyType = string;
    using step_name = string;
    using removeds = vector<keyType>;

    using loop_state = pair<acum, removeds>;

    template<class Arg>
    using loop_gstep = void (*)(Arg &);

    //todo ARG poderia ser pair<string, size>
    using loop_step_pair_state = loop_gstep<loop_state>;

    using clock = std::chrono::steady_clock;
    using time_duration = std::chrono::milliseconds;
    using time_point = std::chrono::time_point<clock>;

    template <size_t steps>
    class loop
    {
        using task_loop_step = loop_step_pair_state;

        // 3 = 1 before hook, 2 task, 3 after hook
        using full_loop_step = array<task_loop_step,3>;

        array<pair<step_name, full_loop_step>, steps> loop_steps;
        task_loop_step before_sleep;
        
       void sleep(loop_state& state,  time_point& time){

        //calculate if based on state, sleep should be shorter than ime_point(time)
        auto until = time;

        std::this_thread::sleep_until(until);
       
       }
    
    public:
        loop(array<full_loop_step, steps> loop):loop_steps(loop){}
        
        void start()
        {
            auto state = make_pair(0L, vector<keyType>{});
            auto time_hooks = array<step_name,steps>{};

            auto run_task = [&state](task_loop_step* task_step){
                (*task_step)(state);
            };
 
            auto run_loop = [](pair<step_name, full_loop_step>& full_step){
                //time hook usando full_step.first
                for_each(full_step.second.begin(), full_step.second.end(),run_task);
                //time hook usando full_step.first
            };

            while (true){
    
                for_each(loop_steps.begin(), loop_steps.end(),run_loop);

                //time hook usando "_main_loop"
                before_sleep(state);
                //time hook usando "_main_loop"

                //todo circular buffer para acum, removeds and timehooks ???

                state.first = 0;
                state.second.clear();

                sleep(state);
                
            }
        }
    };

    steps:
    -update cache
    -time scan - interval based
    -pubsub dispatching - interval based
    -cluster mngmnt
    -io (socket and/or file)

}
