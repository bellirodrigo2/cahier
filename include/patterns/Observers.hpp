#ifndef _DISPATCH_HPP_
#define _DISPATCH_HPP_

#include "PubSub.hpp"
#include "libs.hpp"

namespace baseCahier
{
    using namespace libs;
    using type::pair;
    
    template<typename T>
    using future = libs::future::future<T>;

    using thread::thread_pool;

    template <typename T, typename Result, int size = 128>
    class FileWriterObserver : public Observer<T>
    {
        const string fileName;

        public:
        void operator()(T &source, Entry<T> *entry)
        {
            //async writer
        };
    };

    template <typename T, typename Result, int size = 128>
    class DispatchTaskObserver : public Observer<T>
    {
        using entryResult = pair<EntryHDR, Result>;

        using taskFunc = future<entryResult> (*)(Entry<T> *);
        using thenFunc = void (*)(future<entryResult>);

        taskFunc taskFunc_;
        thenFunc thenFunc_;

    public:
        DispatchTask(taskFunc task_, thenFunc thenFunc_) :taskFunc_(task_), thenFunc_(thenFunc_) {}

        void operator()(T &source, Entry<T> *entry) //todo
        {
            pool.push(taskFunc_, entry, thenFunc_);
        };
    };
}

#endif