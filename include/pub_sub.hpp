#ifndef _PUBSUB_
#define _PUBSUB_

#include <algorithm>

// #include "Api.hpp"
#include "libs.hpp"

#ifdef DEBUG
#include <cassert>
#endif

namespace baseCahier
{
    using namespace libs;
    using libs::thread::thread;
    using s_ptr::unique_ptr;
    using time::clock;
    using time::timePoint;
    using STL::taskQueueSafe;
    using STL::map;

    template <typename Ret, typename... Args>
    using Operation = Ret (*)(Args...);

    struct EntryHDR
    {
        const Hdr node_hdr;
        const size_t entry_id;
        const timePoint since;

        EntryHDR(const Hdr node_hdr, const size_t entry_id)
            : node_hdr(node_hdr), entry_id(entry_id), since(clock::now()) {}
    };

    template <typename T>
    struct Entry
    {
        Entry(const Hdr node_hdr, const size_t entry_id, const unique_ptr<T> data)
            : hdr(EntryHDR(node_hdr, entry_id)), data(std::move(data)) {} // todo definir move no libs

        const EntryHDR hdr;
        const shared_ptr<T> data;

        // todo sizeFunc heree
        size_t size() { return sizeFunc(data); }
    };

    template <typename T>
    class Observer
    {
    public:
        virtual void operator()(T &, Entry<T> *) = 0;
    };

    template <typename T>
    class Observable
    {
        vector<Observer<T>&> observers; //tem que copiar

        void notify(T &source, shared_ptr<vector<T>> entry)
        {
            //shared will guarantee threa safety here
            for (auto observer : observers)
                observer(source, entry);
        }

    public:
        Observable<T>(Observable<T> obs) = default;
        void operator=(Observable<T> obs) = default;
        Observable<T>(Observable<T>& obs) = delete;
        void operator=(Observable<T>& obs) = delete;

        void subscribe(Observer<T> &observer) { observers.push_back(observer); }
        void unsubscribe(Observer<T> &observer)
        {
            observers.erase(
                remove(observers.begin(), observers.end(), observers),
                observers.end());
        }
    };

    template <typename T>
    using ProcessEntry = void (*)(Entry<T> *);

    template <typename T>
    class PubSub 
    {
        //lembrar que cada observer deve ser um consumer group
        taskQueueSafe<Entry<T>> queue;
        Observable<PubSub<T>>& observable;
        // todo
        //need a counter private inheritance
        virtual size_t size() = 0;

        future<vector<unique_ptr<RES>>> assign(){
            auto stolenqueue = queue.steal();
            if(stolenqueue){
                return async(stolenqueue, std::copy(observable));
            }
            return;
        }

    public:
        PubSub(){}
        void addEntry(shared_ptr<Entry<T>> entry)
        {
            queue.push(entry);
            //todo add counter
        }
        void subscribe(Observer<T> &observer) { observable.subscribe(observer);}
        void unsubscribe(Observer<T> &observer){ observable.unsubscribe(observer);}
    };

    template <typename T, typename Result>
    using task = Result (*)(Entry<T> *);
}

#endif