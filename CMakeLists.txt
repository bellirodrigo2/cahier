# run  $ cmake -DCMAKE_BUILD_TYPE=Debug ..

cmake_minimum_required(VERSION 3.22)

set(CMAKE_CXX_STANDARD 17)
SET(CMAKE_CXX_FLAGS "-Wall -Werror")

project(cahier_root)

add_subdirectory(ext/EASTL)

# BUILD LIBRARY libcahier.a
# add_library(cahier
  # STATIC
# )

# target_include_directories(cahier 
    # PUBLIC 
    # include
# )

# #BUILD GTEST
# include(FetchContent)
# FetchContent_Declare(
#   googletest
#   URL https://github.com/google/googletest/archive/609281088cfefc76f9d0ce82e1ff6c30cc3591e5.zip
# )
# # For Windows: Prevent overriding the parent project's compiler/linker settings
# set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
# FetchContent_MakeAvailable(googletest)

# # declares the C++ test binary you want to build (all_tests)
# add_executable(all_tests
#   test/all_tests.cpp
#   test/base_cahier_tests.cpp
#   # test/ret_pol_allfifo_tests.cpp
# )

# # links executable to GoogleTest (gtest_main)
# target_link_libraries(all_tests
#   # cahier
#   gtest_main
#   gmock_main
# )

# include(GoogleTest)
# gtest_discover_tests(all_tests)