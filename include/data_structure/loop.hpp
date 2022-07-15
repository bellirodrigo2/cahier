
#include <string>
#include <vector>
#include <array>
#include <algorithm>
#include <utility>
#include <chrono>
#include <thread>

namespace core
{
    using std::array;
    using std::for_each;
    using std::make_pair;
    using std::pair;
    using std::string;
    using std::vector;

    template <class Arg>
    using loop_step = void (*)(Arg &);

    //TODO da pra deixar os perf hook em outro lyer ????
    //TODO ou usar compiler definition on perf_hook codes

    using clock = std::chrono::steady_clock;
    using time_duration = std::chrono::milliseconds;
    using time_point = std::chrono::time_point<clock>;

    // usar builder para contruit o loop_steps
    template <class state_, size_t steps>
    struct loop_steps_s
    {
        
        loop_step deveria ser um statefull functor template T get_state();
        elimina state_
        como elimina steps recebendo do constructor ???
        array<loop_step<state_>, steps> loop_steps;
        using steps_perf = pair<string, time_duration>;
        array<steps_perf, steps + 1> perf_hooks; //+1 to add before_sleep performance hook
    };

    template <class state_, size_t steps>
    class loop
    {
        state_ state;
        loop_steps_s<state_, steps> loop_steps;
        loop_step<state_> before_sleep;

        void sleep(time_point &time)
        {
            // calculate if based on state, sleep should be shorter than ime_point(time)
            auto until = time;
            std::this_thread::sleep_until(until);
        }

    public:
        loop(loop_steps_s<state_, steps> l_steps, loop_step<state_> b_sleep) : loop_steps(l_steps), before_sleep(b_sleep) {}

        void start()
        {
            auto run_task = [&](loop_step<state_> *task_step)
            {
                // time hook here
                (*task_step)(state);
                // time hook here
            };

            while (true)
            {

                for_each(loop_steps.begin(), loop_steps.end(), run_task);

                // time hook usando "_main_loop"
                before_sleep(state);
                // time hook usando "_main_loop"

                // todo circular buffer para acum, removeds and timehooks ???

                state.first = 0;
                state.second.clear();

                sleep(state);
            }
        }
    };

}
