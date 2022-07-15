#ifndef _CACHE_HPP_
#define _CACHE_HPP_

#include <string>
#include <memory>

namespace cache
{

    using std::string;
    using keyType = string;
    using std::shared_ptr;
    using std::unique_ptr;

    //fazer visitor design pattern com variadic template
    template <class visitor>
    struct visitable
    {
        virtual void accept(visitor &) = 0;
    };

    // compensa fazer map de int e usar hash<string>=>long
    struct list_visitor;
    // use function - lru, lfu, fifo, random, sttl

    template <class T, predicate pop_if_impl>
    class ext_intrusive_list : public visitable<list_visitor>
    {
        virtual unique_ptr<T> pull_out(shared_ptr<T>) = 0;
        virtual void move_next() = 0;
        virtual void move_prev() = 0;

    public:
        virtual void push(node) = 0;
        virtual unique_ptr<T> pop() = 0; // gerar erro se

    };

    template <class T , predicate use_impl, predicate pop_if_impl>
    class cache
    {
        ext_intrusive_list<T, pop_if_impl> list;
        map<keyType, Node> col;

    public:
        virtual shared_ptr<T> get() = 0; // gerar erro se
        void use(node){use_impl();}
        virtual void add() = 0;
        virtual void update() = 0; // gerar erro se
        virtual unique_ptr<T> pull(shared_ptr<T>) = 0;

        // set iterator para map ou list ???
        // begin
        // end
    };
}

#endif