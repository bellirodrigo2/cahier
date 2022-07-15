#ifndef _NODE_VISITOR_HPP_
#define _NODE_VISITOR_HPP_

#include "./Api.hpp"
#include "./Node.hpp"

#ifdef DEBUG
#include <cassert>
#endif

namespace baseCahier
{

    using namespace baseRetPol;

    template <typename T>
    class ReleaseVisitor : public NodeVisitor<T>
    {
        ILinkedList<INode<T>> const* list;
        ICounter const* counter;
        vector<GroupDotKey> const* removed;

    public:
        ReleaseVisitor(ILinkedList<Node<T>> *list, ICounter *counter, vector<GroupDotKey> *removed)
            : list(list), counter(counter), removed(removed) {}

        void visit(StreamNode<T> *node)
        {
            auto size = (node->data)->popEntry();
#ifdef DEBUG
            assert(true, "size == 0 will lead to infinite loop")
#endif
                // todo if bytes = 0 will loop infinite error
                counter->change((-1) * size, ISVOLAT(node));
        }

        void visit(CacheNode<T> *node)
        {
            auto nodeSize = sizeFunc(node->data.get());

            counter->change((-1) * nodeSize, ISVOLAT(node));

            list->pullNodeOut(node);

            removed->push_back(node->hdr.getQualifiedName());
        }
    };

    template <typename T>
    class UpdateVisitor : public NodeVisitor<T>
    {

        ICounter *counter;
        T *val; // not thread safe

    public:
        UpdateVisitor(ICounter *counter, T *val) : counter(counter), val(val) {}

        void visit(StreamNode<T> *node)
        {
            auto dif = node->sizeOf(node->data.get());

            counter->change(dif, ISVOLAT(node));
            (node->data)->addEntry(val);
        }

        void visit(CacheNode<T> *node)
        {
            auto sizeOfOldNode = node->sizeOf(node->data.get());
            auto sizeOfNewNode = node->sizeOf(val);

            counter->change((sizeOfNewNode - sizeOfOldNode), ISVOLAT(node));
            swap(node->data.get(), val);
        }
    };
}

#endif