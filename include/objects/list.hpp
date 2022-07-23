#ifndef CAHIER_LIST_H
#define CAHIER_LIST_H

#include <boost/intrusive/list.hpp>
#include "../patterns/Visitors.hpp"

namespace base_cahier
{
    namespace intrusive_list
    {
        struct node_visitor;

        // single and container
        template <class T, class Hdr>
        struct cnode : public boost::intrusive::list_base_hook<>,
                       visitor::visitable<node_visitor>
        {
            const Hdr hdr;
            const T data;

            cnode(Hdr hdr, T data) : hdr(hdr), data(data) {}
            virtual ~cnode() {}
        };

        template<typename T, typename Hdr>
        class list : boost::intrusive::list<cnode<T, Hdr>>{};

        //for lfu and ttl
        template<typename T, typename Hdr>
        class ordered_list : boost::intrusive::list<cnode<T, Hdr>>{
            void push_back(cnode<T, Hdr>&){};
        };
    }
}
#endif