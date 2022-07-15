#include <gtest/gtest.h>

#ifdef DEBUG
    #include <stdio.h>
#endif

int main(int argc, char **argv) {

#ifdef DEBUG
    printf("********************\nDEBUG on for all_tests.cpp\n********************\n");
#endif

  ::testing::InitGoogleTest(&argc, argv);
  
  return RUN_ALL_TESTS();
}
