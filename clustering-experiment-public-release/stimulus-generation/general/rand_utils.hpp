#pragma once
#include <boost/uuid/uuid_generators.hpp> // generators
#include <random>
extern std::random_device random_device;
extern std::mt19937 mersenne_twister;
extern boost::uuids::basic_random_generator<std::mt19937> uuid_generator;
unsigned int set_seed(unsigned int user_seed);
