#pragma once
#include <boost/uuid/uuid.hpp> // uuid class
#include <iostream>

struct Point {
  int x;
  int y;
  boost::uuids::uuid uuid;

  // Measures the distance between this point and another.
  double distance_to(Point const &other) const;

  // Pretty printing point information.
  friend std::ostream &operator<<(std::ostream &os, Point const &point);

  friend bool operator==(Point const &a, Point const &b);

  // Generate random point
  Point static rand(int max_x, int max_y);

  Point static create(int x, int y);
};
