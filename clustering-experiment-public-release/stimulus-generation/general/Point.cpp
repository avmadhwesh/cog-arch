#include "Point.hpp"
#include "rand_utils.hpp"
#include <boost/uuid/uuid_io.hpp>
#include <cmath>
#include <iostream>

double powi(int n, int exponent) {
  return std::pow(static_cast<double>(n), exponent);
}

double Point::distance_to(Point const &other) const {
  int x1 = x;
  int x2 = other.x;
  int y1 = y;
  int y2 = other.y;

  return std::sqrt(powi(x1 - x2, 2) + powi(y1 - y2, 2));
}

// Pretty printing point information.
std::ostream &operator<<(std::ostream &os, Point const &point) {
  return os << "<Point uuid=" << point.uuid << " x=" << point.x
            << " y=" << point.y << ">";
}

Point Point::rand(int max_x, int max_y) {
  std::uniform_int_distribution<int> rand_x_dist(0, max_x);
  std::uniform_int_distribution<int> rand_y_dist(0, max_y);

  return Point{std::abs(rand_x_dist(mersenne_twister)),
               std::abs(rand_y_dist(mersenne_twister)), uuid_generator()};
}

bool operator==(Point const &a, Point const &b) { return a.uuid == b.uuid; }

Point Point::create(int x, int y) { return Point{x, y, uuid_generator()}; }
