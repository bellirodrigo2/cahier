
    // template <typename T>
    // class Queue
    // {
    //     Entry<T> *front() = 0;
    //     Entry<T> *back() = 0;

    //     virtual void reset() = 0;
    //     virtual bool push(Entry<T> &entry) = 0;
    //     virtual Entry<T> *pop() = 0;
    // };

    // template <typename T, int size>
    // class EntryQueue : public Queue<T>
    // {
    //     static_assert(size != 0, "Size of EntryQueue should be > 0");

    //     const array<Entry<T>, size> queue = array<Entry<T>, size>();
    //     const size_t id;
    //     unsigned start = 0;
    //     unsigned end = 0;

    //     EntryQueue<T, size> *next;
    //     EntryQueue<T, size> *prev;

    // public:
    //     EntryQueue(size_t id) : id(id) {}

    //     // manter essa gambuarra >?
    //     EntryQueue<T, size> *front() { return next; };
    //     EntryQueue<T, size> *back() { return prev; };

    //     void reset() { start = end = next = prev = 0; }
    //     bool push(Entry<T> &entry)
    //     {
    //         // minoria das vezes 1 em 'size' times
    //         if (end == size)
    //             return false;

    //         queue[end++] = entry;
    //         return true;
    //     };

    //     Entry<T> *pop()
    //     {
    //         return (start == end) ? nullptr : &queue[start++];
    //     };
    // };

    // template <typename T, int size>
    // class EntryChain : public Queue<T>
    // {
    //     static_assert(size != 0, "Size of EntryChain should be > 0");

    //     static size_t id_generator;
    //     EntryQueue<T, size> *front_{nullptr};
    //     EntryQueue<T, size> *back_{nullptr};

    //     EntryQueue<T, size> *MAKEQUEUE()
    //     {
    //         return new EntryQueue<T, size>{id_generator++};
    //     }

    // public:
    //     EntryChain()
    //     {
    //         front_ = back_ = MAKEQUEUE();
    //     }
    //     ~EntryChain()
    //     {
    //         // iterate and delete using algoritm. checkar se eles nao throw
    //         // guarantir no throw
    //     }

    //     EntryQueue<T, size> *front() { return front_; }
    //     EntryQueue<T, size> *back() { return back_; }

    //     void reset()
    //     {
    //         back_ = front_;
    //         front_->reset();
    //     }

    //     bool push(Entry<T> &entry)
    //     {
    //         if (!back_->push(entry))
    //         {
    //             auto newNode = MAKEQUEUE();
    //             back_->next = newNode;
    //             newNode->prev = back_;
    //             back_ = newNode;
    //             return back_->push(entry);
    //         }
    //         return true;
    //     };

    //     Entry<T> *pop()
    //     {
    //         auto popped = front_->pop();
    //         if (popped)
    //             return popped;

    //         if (front_ == back_)
    //         {
    //             front_->reset();
    //             return nullptr;
    //         }
    //         else
    //         {
    //             front_->next->prev = nullptr;
    //             front_ = front_->next;
    //             front_->next = nullptr;
    //             return front_->pop();
    //         }
    //     };
    // };
