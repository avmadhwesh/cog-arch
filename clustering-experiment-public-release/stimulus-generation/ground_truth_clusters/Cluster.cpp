#include "Cluster.hpp"
#include "Point.hpp"
#include "Settings.hpp"
#include "rand_utils.hpp"
#include <boost/uuid/uuid_io.hpp>
#include <cmath>
#include <iostream>
#include <random>
#include <vector>

Cluster
Cluster::make_from_centroid(Point const &centroid, Settings const &settings,
                            std::vector<Cluster> const &preexisting_clusters) {

  auto standard_deviation = settings.standard_deviation;
  auto points_per_cluster = settings.points_per_cluster;
  auto min_point_distance = settings.min_point_distance;

  std::vector<Point> points;
  std::normal_distribution x_norm{static_cast<double>(centroid.x),
                                  standard_deviation};
  std::normal_distribution y_norm{static_cast<double>(centroid.y),
                                  standard_deviation};

  while (points.size() != points_per_cluster) {

    int x = static_cast<int>(std::round(x_norm(mersenne_twister)));
    int y = static_cast<int>(std::round(y_norm(mersenne_twister)));

    // Prevent negative points.
    if (x < 0 || y < 0) {
      continue;
    }

    auto candidate_point = Point::create(x, y);
    bool too_close = false;

    // Check with current cluster points.
    for (auto &&preexisting_point : points) {
      auto dist = candidate_point.distance_to(preexisting_point);
      if (dist < min_point_distance) {
        too_close = true;
        break;
      }
    }

    if (too_close)
      continue;

    // Check with other cluster points.
    for (auto &&preexisting_cluster : preexisting_clusters) {
      for (auto &&preexisting_point : preexisting_cluster.points) {
        auto dist = candidate_point.distance_to(preexisting_point);
        if (dist < min_point_distance) {
          too_close = true;
          break;
        }
      }
      if (too_close) {
        break;
      }
    }

    if (too_close)
      continue;

    points.push_back(std::move(candidate_point));
  }

  return Cluster{centroid, points, uuid_generator()};
}

// Pretty printing cluster information.
std::ostream &operator<<(std::ostream &os, Cluster const &cluster) {
  os << "<Cluster uuid=" << cluster.uuid << " centroid=" << cluster.centroid
     << " points=[";

  auto point_size = cluster.points.size();
  for (decltype(cluster.points)::size_type i = 0; i < point_size; i++) {
    os << cluster.points[i];
    if (i != point_size - 1) {
      os << ", ";
    }
  }

  os << "]>";
  return os;
}
