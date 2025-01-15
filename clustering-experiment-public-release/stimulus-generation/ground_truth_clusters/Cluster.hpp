#pragma once
#include "Point.hpp"
#include "Settings.hpp"
#include <boost/uuid/uuid.hpp>
#include <vector>
struct Cluster {
  Point centroid;
  std::vector<Point> points;
  boost::uuids::uuid uuid;

  // Generates a cluster from a centroid, settings, and existing
  // clusters.
  static Cluster
  make_from_centroid(Point const &centroid, Settings const &settings,
                     std::vector<Cluster> const &preexisting_clusters);

  // Pretty printing cluster information.
  friend std::ostream &operator<<(std::ostream &os, Cluster const &cluster);
};
