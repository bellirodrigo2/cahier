#ifndef CAHIER_LIST_H
#define CAHIER_LIST_H

#include <boost/intrusive/list.hpp>
#include <chrono>
#include <deque>
#include <list>
#include <memory>

#include "patterns/Visitor.hpp"

namespace base_cahier
{
    namespace cache_list
    {
        using namespace visitor;

        using boost::intrusive::list_base_hook;
        using std::shared_ptr;
        using std::deque;
        using std::list;

		using namespace std::chrono;
        using clock = steady_clock;
        using timeDuration = milliseconds;
        using timePoint = time_point<clock>;

        template<typename T>
        struct node_visitor;

        //NODE API
        template <typename T>
        struct node : public list_base_hook<>, visitable<node_visitor<T>>
        {
            T data;
            const timePoint since;
            timeDuration timeout;
            size_t uses;

            node(T data, timePoint since, timeDuration timeout) : 
                data(data), since(since), timeout(timeout), uses(0){}
            virtual ~node(){}
        };

        template <typename T>
        struct val_node : public node<T>{};
        template<typename T>
        node<T> make_node(T data, timePoint since, timeDuration timeout){}

        template <typename T>
        struct sptr_node : public node<shared_ptr<T>>{};
        template<typename T>
        node<T> make_node(shared_ptr<T> data, timePoint since, timeDuration timeout){}

        template <typename T>
        struct deque_node : public node<deque<T>>{};
        template<typename T>
        node<T> make_node(deque<T> data, timePoint since, timeDuration timeout){}

        template <typename T>
        struct list_node : public node<list<T>>{};
        template<typename T>
        node<T> make_node(list<T> data, timePoint since, timeDuration timeout){}

        // template <typename T>
        // struct pub_sub_node : public node<pub_sub<T>>{};

        template<typename T>
        struct node_visitor{
            void visit(val_node<T>);
            void visit(sptr_node<T>);
            void visit(deque_node<T>);
            void visit(list_node<T>);
            // void visit(pub_sub_node<T>);
        };


        //LIST API

        //for lru, fifo and random
        template<typename T>
        class ilist : boost::intrusive::list<node<T>>{};

        //for lfu and ttl
        template<typename T>
        class ordered_list : ilist<T>{
            void push_back(node<T>&){}; //this should be an override
        };
    }
}
#endif