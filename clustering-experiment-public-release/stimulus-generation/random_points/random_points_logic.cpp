#include "random_points_logic.hpp"
#include "Point.hpp"
#include "measures.hpp"
#include "rand_utils.hpp"
#include <iostream>
#include <vector>

std::vector<Point> generate_points(int n_points) {

  std::uniform_int_distribution x_dist(CANVAS_MARGIN,
                                       CANVAS_WIDTH - CANVAS_MARGIN);
  std::uniform_int_distribution y_dist(CANVAS_MARGIN,
                                       CANVAS_HEIGHT - CANVAS_MARGIN);
  std::vector<Point> points;
  points.push_back(
      Point::create(x_dist(mersenne_twister), y_dist(mersenne_twister)));
  while (points.size() != n_points) {
    auto candidate =
        Point::create(x_dist(mersenne_twister), y_dist(mersenne_twister));
    bool too_close = false;
    for (auto &&existing_point : points) {
      auto dist = candidate.distance_to(existing_point);
      if (dist < MIN_POINT_DISTANCE) {
        too_close = true;
      }
    }
    if (!too_close) {
      points.push_back(candidate);
    }
  }

  return points;
}
