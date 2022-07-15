#ifndef _NODE_IMPL_HPP
#define _NODE_IMPL_HPP

#include "Api.hpp"
#include "libs.hpp"

namespace baseCahier
{

    using namespace baseCahier;
    using namespace libs;
    using STL::map;
    using STL::set;
    using STL::vector;
    using STL::vectorNull;

    template <typename K>
    struct Hook : IHook<K>
    {
    };

    template<typename T>
    class NodegVisitor;

    template <typename T>
    struct Node : public INode<T>
    {
        Node(Hdr hdr, T &data) : INode<T>(hdr, std::move(data)) {} // todo declarar move
    };

    template <typename T>
    struct vectorNode : public Node<vector<T>>{};

    template <typename T>
    struct vectorNullNode : public Node<vectorNull<T>>{};

    template <typename T>
    struct setNode;

    template <typename T>
    struct listNode;

    template <typename T>
    struct mapNode;

    template <typename T>
    struct streamNode;

    //fazer todos scopeds

    template <typename T>
    class NodegVisitor
    {
        // https://stackoverflow.com/questions/11796121/implementing-the-visitor-pattern-using-c-templates
    public:
        virtual void visit(Node<T>*)=0;
        virtual void visit(vectorNode<T>*)=0;
        virtual void visit(setNode<T>*)=0;
        virtual void visit(listNode<T>*)=0;
        virtual void visit(mapNode<T>*)=0;
        virtual void visit(streamNode<T>*)=0;
    };
}

#endif