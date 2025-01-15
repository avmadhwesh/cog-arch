#include "rand_utils.hpp"
#include <boost/uuid/uuid_generators.hpp>
#include <random>
std::random_device random_device;
std::mt19937 mersenne_twister(random_device());
boost::uuids::basic_random_generator<std::mt19937>
    uuid_generator(mersenne_twister);

// returns the seed that was used
unsigned int set_seed(unsigned int user_seed) {
  if (user_seed != 0) {
    // If seed is not 0, reseed the mersenne_twister with the seed.
    // If the seed is 0, the default random device seed will be used. See
    // rand_utils.{hpp,cpp}
    mersenne_twister.seed(user_seed);
    return user_seed;
  } else {
    unsigned int seed = 0;
    while (seed == 0) {
      std::uniform_int_distribution<unsigned int> int_dist;
      seed = int_dist(mersenne_twister);
    }
    mersenne_twister.seed(seed);
    return seed;
  }
}
