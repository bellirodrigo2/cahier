#ifndef CAHIER_NODE_VISITOR_H
#define CAHIER_NODE_VISITOR_H

#include "../list.hpp"

namespace visitor_impl{

    using namespace base_cahier::cache_list;

    template<typename T>
    struct update_visitor : public node_visitor<T>{
        void visit(val_node<T>);
        void visit(sptr_node<T>);
        void visit(deque_node<T>);
        void visit(list_node<T>);
        // void visit(pub_sub_node<T>);

        private:
        T new_val;
    };

    template<typename T>
    struct release_memory_visitor : public node_visitor<T>{
        void visit(val_node<T>);
        void visit(sptr_node<T>);
        void visit(deque_node<T>);
        void visit(list_node<T>);
        // void visit(pub_sub_node<T>);

        private:
        size_t size;
    };


    template<typename T>
    struct sizeof_visitor : public node_visitor<T>{
        void visit(val_node<T>);
        void visit(sptr_node<T>);
        void visit(deque_node<T>);
        void visit(list_node<T>);
        // void visit(pub_sub_node<T>);
    };
}
#endif