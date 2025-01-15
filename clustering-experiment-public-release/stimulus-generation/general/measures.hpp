#pragma once
#include "Point.hpp"
#include <vector>
namespace measures {
struct MeasureInformation {
  int n_points;
  int canvas_width;
  int canvas_height;
};

double z_score(std::vector<Point> const &points,
               MeasureInformation const &measure_info);
double vacuumed_z_score(std::vector<Point> const &points);
} // namespace measures
