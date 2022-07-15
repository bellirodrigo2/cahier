#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include <tuple>
#include <vector>
#include <iostream>
#include <memory>

#include "../include/RetentionPolicy.hpp"
#include "../include/Node.hpp"

using namespace baseRetPol;
using namespace baseCahier;
using namespace std;
using namespace testing;

size_t sizeOfInt(int* val){return sizeof(int);};

class LinkedListMock :public ILinkedList<INode<int>>{

    public:
    ~LinkedListMock(){}
    MOCK_METHOD(void, push, (INode<int>*));
    MOCK_METHOD(INode<int>*, pop, ());
    MOCK_METHOD(void, pullNodeOut, (INode<int>*));
    MOCK_METHOD(bool, moveNodeNext, (INode<int>*));

    using iterator = ILinkedList<INode<int>>::iterator;

    MOCK_METHOD(iterator, begin, ());
    MOCK_METHOD(iterator, end, ());

};

class CounterMock :public ICounter{

    public:
    ~CounterMock(){}
    MOCK_METHOD(void, change, (long, bool));
    MOCK_METHOD(size_t, available, ());
    MOCK_METHOD(size_t, all, ());
    MOCK_METHOD(size_t, volat, ());
    MOCK_METHOD(size_t, nonvolat, ());
    MOCK_METHOD(size_t, max, ());
};

template<typename T>
size_t unit(T * data){return 1;};

struct RetPolTest : public ::testing::Test
{
protected:

    LinkedListMock* list = new LinkedListMock{};
    CounterMock* counter = new CounterMock{};
    AllFIFO<int>* rp = MAKE_FIFO_ALL<int>(list,counter);

    public:
    ~RetPolTest(){delete rp;}
};

TEST_F(RetPolTest, Use) {

    string key{"hello"};
    string group{"group"};
    objectOption opt{100};

    int num = 45;
    auto hdr = Hdr{key, group, opt.timeout};
    auto sptr = new Node<int>(hdr,&num, &sizeOfInt);
    
    EXPECT_CALL(*list, pullNodeOut);
    EXPECT_CALL(*list, push);
    
    rp->use(sptr);

}
