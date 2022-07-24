#ifndef CAHIER_CACHE_H
#define CAHIER_CACHE_H

#include <unordered_map>
#include <optional>
#include "list.hpp"

#include "visitors/node_visitor.hpp"

namespace base_cahier
{
	using namespace cache_list;
	using std::unordered_map;
	using size_t = unsigned long;
	using std::optional;
	using std::nullopt;
	using namespace visitor_impl;

	// allkeys, volatkeys
	template <typename T>
	using Predicate = bool (*)(node<T>);

	// lru, lfu, ttl, fifo, random
	template <typename T>
	using ListNodeOperation = void (*)(list<T> &, node<T> &);

	template <typename Value, typename Key,
			  Predicate<Value> keys_func, ListNodeOperation<Value> touch_func,
			  typename List = ilist<Value>, typename Map = unordered_map<Key, node<Value>>>
	class cache
	{
	public:
		using key_type = Key;
		using value_type = Value;
		using container_type = node<value_type>;
		using list_type = List;
		using map_type = Map;
		using keys_strategy = Predicate<value_type>;
		using cache_strategy = ListNodeOperation<Value>;
		using size_type = size_t;
		using iterator = typename list_type::iterator;
		using const_iterator = typename list_type::const_iterator;
		using this_type = cache<value_type, key_type, keys_func, touch_func, list_type, map_type>;

		cache(size_t capacity)
			: m_list(list_type()),
			  m_map(map_type()),
			  m_capacity(capacity),
			  m_all(0),
			  m_volat(0) {}
		~cache() {}

		cache(const this_type &) = delete;
		this_type &operator=(const this_type &) = delete;

		// GETTERS
		optional<value_type> get(const key_type &k)
		{
			auto iter = m_map.find(k);

			if (iter == m_map.end()) return nullopt;
			touch(k);
			return iter->data;
		}

		optional<value_type> at(const key_type &k)
		{
			auto iter = m_map.find(k);
			return (iter != m_map.end()) ? iter->data : nullopt;
		}

		inline value_type &operator[](const key_type &k) { return get(k); }

		// SETTERS
		//emplace(){} //usando make_node

		bool insert(const key_type &k, const value_type &v)
		{
			if (m_map.find(k) != m_map.end())
				return false;
			make_space(sizeof_visitor<Value>{});
			m_list.push_front(k);
			m_map[k] = v;
			return true;
		}

		void insert_or_assign(const key_type &k, const value_type &v)
		{
			auto iter = m_map.find(k);
			iter != m_map.end() ? assign(iter, v) : insert(k, v);
		}

		bool assign(const key_type &k, const value_type &v)
		{
			auto iter = m_map.find(k);
			if (iter == m_map.end())
				return false;
			assign(iter, v);
			return true;
		}

		void assign(iterator &iter, const value_type &v)
		{
			touch(iter);

			//todo visitor here
			iter->accept(update_visitor<Value>{v});
			// iter->data = v;
			// iter->data.push_back(v);
		}

		// CONTAINS
		inline bool contains(const key_type &k) const
		{
			return m_map.find(k) != m_map.end();
		}

		// REMOVE
		bool erase(const key_type &k) {}
		bool erase(iterator &it) {}

		void release_memory(size_t size){
			auto iter = begin(); //todo begin ou rbegin ?????
			iter->accept(release_memory_visitor<Value>{size});
		}

		// ITERATORS
		iterator begin() noexcept { return m_list.begin(); }
		iterator end() noexcept { return m_list.end(); }
		iterator rbegin() noexcept { return m_list.rbegin(); }
		iterator rend() noexcept { return m_list.rend(); }
		const_iterator begin() const noexcept { return m_list.begin(); }
		const_iterator cbegin() const noexcept { return m_list.cbegin(); }
		const_iterator crbegin() const noexcept { return m_list.crbegin(); }
		const_iterator end() const noexcept { return m_list.end(); }
		const_iterator cend() const noexcept { return m_list.cend(); }
		const_iterator crend() const noexcept { return m_list.crend(); }

		// SIZING
		bool empty() const noexcept { return m_map.empty(); }
		size_type size() const noexcept { return m_all; }
		size_type volat() const noexcept { return m_volat; }
		size_type capacity() const noexcept { return m_capacity; }

		void filter_scan(){
			auto iter = begin(); //ou rbgein ?
			//! usar predicate
			//iterar e erase se predicate
		}

	private:
		bool touch(const key_type &k){}
		void touch(iterator &it){}

		void make_space(size_t size){
			auto iter = begin(); //ou rbgein ?
			//! usar keys_func
			//iterar e erase ateh acumular size
			//usar std::algorithms ???	
		}

		list_type m_list;
		map_type m_map;
		size_type m_capacity;
		size_type m_all;
		size_type m_volat;
	};
}
#endif
