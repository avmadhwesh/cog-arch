#include "measures.hpp"
#include "Point.hpp"
#include <algorithm>
#include <cmath>
#include <limits>
#include <vector>

namespace measures {

double nearest_neighbor_distance(Point const &point,
                                 std::vector<Point> const &all_points) {
  double min_distance = std::numeric_limits<double>::max();
  for (auto &&every_point : all_points) {
    if (point == every_point)
      continue;
    auto dist = point.distance_to(every_point);
    if (dist < min_distance)
      min_distance = dist;
  }
  return min_distance;
}

double mean_nearest_neighbor_distance(std::vector<Point> const &points) {
  double sum = 0;
  for (auto &&point : points) {
    sum += nearest_neighbor_distance(point, points);
  }
  return sum / points.size();
}

double expected_random_nearest_neighbor_distance(
    MeasureInformation const &measure_info) {

  // Casting everything to double to retain precision.

  // number of points
  double N = measure_info.n_points;
  // area of canvas
  double A = measure_info.canvas_width * measure_info.canvas_height;
  // perimeter of canvas
  double B = 2 * (measure_info.canvas_width + measure_info.canvas_height);

  auto term1 = 0.5 * std::sqrt(A / N);
  auto term2 = (0.0514 + 0.041 / std::sqrt(N)) * (B / N);
  return term1 + term2;
}

double
var_mean_nearest_neighbor_distance(MeasureInformation const &measure_info) {
  // number of points
  double N = measure_info.n_points;
  // area of canvas
  double A = measure_info.canvas_width * measure_info.canvas_height;
  // perimeter of canvas
  double B = 2 * (measure_info.canvas_width + measure_info.canvas_height);

  return (0.070 * A / std::pow(N, 2)) +
         (0.037 * B * std::sqrt(A / std::pow(N, 5)));
}

double z_score(std::vector<Point> const &points,
               MeasureInformation const &measure_info) {
  return (mean_nearest_neighbor_distance(points) -
          expected_random_nearest_neighbor_distance(measure_info)) /
         std::sqrt(var_mean_nearest_neighbor_distance(measure_info));
}

double vacuumed_z_score(std::vector<Point> const &points) {

  std::vector<int> x_vals;
  std::vector<int> y_vals;

  for (auto &&point : points) {
    x_vals.push_back(point.x);
    y_vals.push_back(point.y);
  }

  const auto [x_min, x_max] = std::minmax_element(x_vals.begin(), x_vals.end());
  const auto [y_min, y_max] = std::minmax_element(y_vals.begin(), y_vals.end());

  MeasureInformation measure_info{.n_points = static_cast<int>(points.size()),
                                  .canvas_width = *x_max - *x_min,
                                  .canvas_height = *y_max - *y_min};

  return z_score(points, measure_info);
};

} // namespace measures
