#ifndef CAHIER_CACHE_H
#define CAHIER_CACHE_H

#include <unordered_map>
#include <optional>
#include "list.hpp"

namespace base_cahier
{
	namespace objects
	{
		using namespace intrusive_list;

		// allkeys, volatkeys
		template <class Hdr>
		using predicate = bool (*)(Hdr);

		// lru, lfu, ttl, fifo, random
		template <typename T, class Hdr>
		using cache_strategy = void (*)(list<T, Hdr> &, Hdr &);

		template <typename T, typename Hdr, typename Key,
				  predicate<Hdr> keys_func, cache_strategy<T, Hdr> use_func,
				  typename list_type = list<T, Hdr>,
				  typename map_type = std::unordered_map<Key, cnode<T, Hdr>>>
		class cache
		{
		public:
			using key_type = Key;
			using value_type = T;
			using data_container_type = cnode<T, Hdr>;
			using size_type = size_t;
			using iterator = typename list_type::iterator;
			using const_iterator = typename list_type::const_iterator;
			using this_type = cache<key_type, T, Hdr, keys_func, use_func, map_type>;

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
			value_type &get(const key_type &k) {}
			std::optional<value_type> at(const key_type &k) {}
			value_type &operator[](const key_type &k) { return get(k); }

			// SETTERS

			/// insert
			/// insert key k with value v.
			/// If key already exists, no change is made and the return value is false.
			/// If the key doesn't exist, the data is added to the map and the return value is true.
			bool insert(const key_type &k, const data_container_type &v)
			{
				if (m_map.find(k) != m_map.end())
					return false;
				make_space(1); // precisa de size aqui
				m_list.push_front(k);
				m_map[k] = v;
				return true;
			}

			template <typename... Args>
			void emplace(const key_type &k, Args &&...args) {}
			void insert_or_assign(const key_type &k, const value_type &v) {}
			bool assign(const key_type &k, const value_type &v) {}
			void assign(iterator &iter, const value_type &v) {}

			// CONTAINS
			bool contains(const key_type &k) const {}

			// REMOVE
			bool erase(const key_type &k) {}
			bool erase(iterator &it) {}
			void erase_tgt() {} // erase according to key_func

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

			// filter based on keys_func using list iterator
			void filter() {}

		private:
			bool touch(const key_type &k) {}
			void touch(iterator &it) {}

			void make_space(size_t size) {}

			list_type m_list;
			map_type m_map;
			size_type m_capacity;
			size_type m_all;
			size_type m_volat;
		};
	}
}
#endif
