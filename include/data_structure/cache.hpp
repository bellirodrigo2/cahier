#ifndef _CACHE_HPP_
#define _CACHE_HPP_

#include <string>
#include <memory>
#include <include/EASTL/intrusive_list.h>
// #include <intrusive_list.h>
#include "../patterns/Visitors.hpp"

namespace cache
{
    using std::string;
    using keyType = string;
    using std::shared_ptr;
    using std::unique_ptr;

    // compensa fazer map de int e usar hash<string>=>long?

    struct list_visitor;
    // use function - lru, lfu, fifo, random, sttl
    
    struct node_visitor;
    //type de nodes dependendo do T

    using visitor::visitable;

    template<class T, class nHDR>
    class cnode:public intrusive_list_node, visitable<node_visitor>{

        nHDR hdr;
        T data;
    };

    template<class T, class nHDR>
    using predicate = bool (*)(cnode);

    template <class T, class nHDR, predicate<T, nHDR> pop_if_impl>
    class ext_intrusive_list : public visitable<list_visitor>
    {
        using cnode_ = cnode<T, nHDR>;
        using cnode_uptr  = unique_ptr<cnode_>;
        using cnode_sptr  = shared_ptr<cnode_>;

        virtual cnode_uptr pull_out(cnode_sptr) = 0;
        virtual void move_next() = 0;
        virtual void move_prev() = 0;

    public:
        virtual void push(cnode_uptr) = 0;
        virtual cnode_uptr pop() = 0; // gerar erro se
    };

    template <class T, class nHDR, 
        predicate<T, nHDR> use_impl, 
        predicate<T, nHDR> pop_if_impl>
    class cache
    {
        using cnode_ = cnode<T, nHDR>;
        using cnode_uptr  = unique_ptr<cnode_>;
        using cnode_sptr  = shared_ptr<cnode_>;

        //list id replicado nos nodes constexpr
        ext_intrusive_list<T, nHDR, pop_if_impl> list;
        hash_map<key_t, cnode_> col;

    public:
        cnode_sptr get() = 0; // gerar erro se
        void use(cnode_& node){use_impl(node);}
        void add(cnode_uptr) = 0;
        void update(cnode_sptr, T) = 0; // gerar erro se
        cnode_uptr pull(cnode_sptr) = 0;
        vector<key_t> scan_clean(predicate) = 0;

        // set iterator para map ou list ???
    };
}

#endif