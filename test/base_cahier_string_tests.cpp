#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include <map>
#include <vector>
#include <iostream>
#include <memory>

#include "../include/BaseCahier.hpp"

using namespace baseCahier;
using namespace std;
using namespace testing;

class RetPolMock : public IRetentionPolicy<string>
{

public:
    ~RetPolMock() {}
    MOCK_METHOD(void, use, (INode<string> *));
    MOCK_METHOD(vector<keyType>, add, (INode<string> *, objectOption));
    MOCK_METHOD(vector<keyType>, update, (INode<string> *, string *));
    MOCK_METHOD(void, pull, (INode<string> *));

    MOCK_METHOD(size_t, max, ());

    MOCK_METHOD(size_t, all, ());
    MOCK_METHOD(size_t, volat, ());
    MOCK_METHOD(size_t, nonvolat, ());
    MOCK_METHOD(size_t, available, ());
    MOCK_METHOD(timePoint, lastScan, ());
};

struct BaseCahierTest : public ::testing::Test
{
protected:
    RetPolMock *rp = new RetPolMock{};
    map<string, string> *col = new map<string, string>{};

    BaseCahier<string> *cahier =new BaseCahier<string>(rp, col);

    string key{"hello"};
    string group{"world"};
    string num{"45"};
    objectOption opt{100};

    vector<keyType> vec{"scopeOne.KeyOne", "scopeTwo.KeyTwo", "scopeThree.KeyThree"};

public:
    ~BaseCahierTest() { delete cahier; }
};

TEST_F(BaseCahierTest, GetNull)
{

    //col is no longer a mock
    // EXPECT_CALL(*col, get(key)).Times(2);

    auto noAnswer = cahier->get(key);
    auto noAnswer2 = cahier->peek(key);
    ASSERT_TRUE(noAnswer.expired());
    ASSERT_TRUE(noAnswer2.expired());
}

TEST_F(BaseCahierTest, GetOK)
{

    auto hdr = Hdr{key, opt.timeout};
    auto sptr = new INode<string>(hdr, &num);

    //col is no longer a mock
    // EXPECT_CALL(*col, get(key)).WillOnce(Return(sptr));
    EXPECT_CALL(*rp, use);

    auto answer = cahier->get(key);

    ASSERT_FALSE(answer.expired());
}

TEST_F(BaseCahierTest, SetNull)
{

    bool hasSet = cahier->set(key, nullptr, opt);
    ASSERT_FALSE(hasSet);
}

TEST_F(BaseCahierTest, SetExisting)
{

    // EXPECT_CALL(*col, has(key)).WillOnce(Return(true));

    bool hasSet = cahier->set(key, &num, opt);
    ASSERT_FALSE(hasSet);
}

TEST_F(BaseCahierTest, SetOK)
{

    // EXPECT_CALL(*col, has(key, group)).WillOnce(Return(false));
    // EXPECT_CALL(*col, set).WillOnce(Return(true));
    EXPECT_CALL(*rp, add);

    bool hasSet = cahier->set(key, &num, opt);
    ASSERT_TRUE(hasSet);
}

TEST_F(BaseCahierTest, SetAndRemove)
{

    // EXPECT_CALL(*col, has(key, group)).WillOnce(Return(false));
    EXPECT_CALL(*rp, add).WillOnce(Return(vec));
    // EXPECT_CALL(*col, remove).Times(vec.size());
    // EXPECT_CALL(*col, set).WillOnce(Return(true));

    bool hasSet = cahier->set(key, &num, opt);
    ASSERT_TRUE(hasSet);
}

TEST_F(BaseCahierTest, UpdateNull)
{

    bool hasSet = cahier->update(key, nullptr);
    ASSERT_FALSE(hasSet);
}

TEST_F(BaseCahierTest, UpdateNonExisting)
{

    // EXPECT_CALL(*col, get(key, group)).WillOnce(ReturnNull());

    bool hasSet = cahier->update(key, &num);
    ASSERT_FALSE(hasSet);
}

TEST_F(BaseCahierTest, UpdateExisting)
{

    string num2{47};

    auto hdr = Hdr{key, opt.timeout};
    auto sptr = new INode<string>(hdr, &num);

    // EXPECT_CALL(*col, get(key, group)).WillOnce(Return(sptr));
    EXPECT_CALL(*rp, update);

    bool hasSet = cahier->update(key, &num2);
    ASSERT_TRUE(hasSet);
}

TEST_F(BaseCahierTest, RemoveNonExisting)
{

    // EXPECT_CALL(*col, get(key, group)).WillOnce(ReturnNull());

    auto removed = cahier->remove(key);
    ASSERT_TRUE(removed == nullptr);
}

TEST_F(BaseCahierTest, RemoveExisting)
{

    auto hdr = Hdr{key, opt.timeout};
    auto sptr = new INode<string>(hdr, &num);

    // EXPECT_CALL(*col, get(key)).WillOnce(Return(sptr));
    EXPECT_CALL(*rp, pull);
    // EXPECT_CALL(*col, remove);

    auto hasRemoved = cahier->remove(key);
    ASSERT_EQ(hasRemoved.get(), &num);
}