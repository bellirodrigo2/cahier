#include <string>
#include <memory>
#include <future>

    template<class OPT, class scope_t = std::string>
    class scope_option :public OPT{
        scope_t scope;
    };

    class loop_control{

        //fazer attributes here like proxy creature c++ degign pattern course

        template<typename T>
        void set(T newVal);
        // intervals, scan, etc
    };

    template<class T, class OPT, class key_t = std::string const&>
    class cahier : loop_control{

        using t_sptr = std::shared_ptr<T>;
        using t_uptr = std::unique_ptr<T>;

        template<typename U>
        using future = std::future<U>;

        //loop + array<steps>
            // steps : 
            //-update cache 
            //- time scan 
            //- interval based 
            //- pubsub dispatching based on interval or not
            //- cluster mngmnt 
            //- io(socket and / or file)
            //loop_control set or get
        //loop control
        //task_queue_safe
        //cache

        public:
            virtual future<t_sptr>  get    (key_t) const = 0;
            virtual future<t_uptr>  getdel (key_t) const = 0;
            virtual future<t_sptr>  peek   (key_t) const = 0;
            virtual future<bool>    set    (key_t, t_uptr, OPT) = 0;
            virtual future<bool>    update (key_t, t_uptr, OPT) = 0;
            virtual future<t_sptr>  remove (key_t) = 0;
    };

    template<class T, class OPT, class key_t = std::string const&>    
    using scope_cahier = cahier<T, scope_option<OPT>, key_t>;
