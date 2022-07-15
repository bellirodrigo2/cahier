#include <iostream>
#include <string>
using namespace std;

// 1. Add an accept(Visitor) method to the "element" hierarchy
class Element
{
public:
  virtual void accept(class Visitor &v) = 0;
};

class This : public Element
{
public:
  /*virtual*/ void accept(Visitor &v);
  string thiss()
  {
    return "This";
  }
};

class That : public Element
{
public:
  /*virtual*/ void accept(Visitor &v);
  string that()
  {
    return "That";
  }
};

class TheOther : public Element
{
public:
  /*virtual*/ void accept(Visitor &v);
  string theOther()
  {
    return "TheOther";
  }
};

// 2. Create a "visitor" base class w/ a visit() method for every "element" type
class Visitor
{
public:
  virtual void visit(This *e) = 0;
  virtual void visit(That *e) = 0;
  virtual void visit(TheOther *e) = 0;
};

/*virtual*/ void This::accept(Visitor &v)
{
  v.visit(this);
}

/*virtual*/ void That::accept(Visitor &v)
{
  v.visit(this);
}

/*virtual*/ void TheOther::accept(Visitor &v)
{
  v.visit(this);
}

// 3. Create a "visitor" derived class for each "operation" to do on "elements"
class UpVisitor : public Visitor
{
  /*virtual*/ void visit(This *e)
  {
    cout << "do Up on " + e->thiss() << '\n';
  }
  /*virtual*/ void visit(That *e)
  {
    cout << "do Up on " + e->that() << '\n';
  }
  /*virtual*/ void visit(TheOther *e)
  {
    cout << "do Up on " + e->theOther() << '\n';
  }
};

class DownVisitor : public Visitor
{
  /*virtual*/ void visit(This *e)
  {
    cout << "do Down on " + e->thiss() << '\n';
  }
  /*virtual*/ void visit(That *e)
  {
    cout << "do Down on " + e->that() << '\n';
  }
  /*virtual*/ void visit(TheOther *e)
  {
    cout << "do Down on " + e->theOther() << '\n';
  }
};

class Base
{

  class MyVisitor : public UpVisitor
  {
  };
  MyVisitor vis{};

public:
  void run();
};

#include "./MAKE.hpp"

int sizeOfInt(){return sizeof(int);};

int main()
{
  Element *list[] =
      {
          new This(), new That(), new TheOther()};
  UpVisitor up;     // 4. Client creates
  DownVisitor down; //    "visitor" objects
  for (int i = 0; i < 3; i++)
    list[i]->accept(up);

  for (int i = 0; i < 3; i++)
    list[i]->accept(down);

  size_t size = 3;
  size -= 4;
  cout << size << endl;

  auto obj = MAKECACHENODE<&sizeOfInt>();

  obj->run();

  string hello{"helo world"};
  char* s_ptr = &hello[0]; // get at the buffer

  for (size_t i = 0; i < 4; i++)
  {
    cout<< s_ptr[i];
  }
  cout<<endl;
  cout<<hello.size()<<endl;
  
}