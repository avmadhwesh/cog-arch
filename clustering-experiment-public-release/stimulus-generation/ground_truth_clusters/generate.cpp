#include "Cluster.hpp"
#include "Point.hpp"
#include "Settings.hpp"
#include "json.hpp"
#include "make_centroids.hpp"
#include "measures.hpp"
#include "rand_utils.hpp"
#include <boost/uuid/uuid_io.hpp> // to_string
#include <random>
#include <sstream>
#include <string>
#include <vector>

using json = nlohmann::json;

json make_json(std::vector<Cluster> const &clusters, Settings const &settings) {

  std::stringstream csv;

  std::vector<Point> combined_points;

  for (auto &&cluster : clusters) {
    // copy operation
    for (Point point : cluster.points) {
      combined_points.push_back(point);
    }
  }

  measures::MeasureInformation measure_info{
      .n_points = settings.points_per_cluster * settings.n_clusters,
      .canvas_width = settings.canvas_width,
      .canvas_height = settings.canvas_height};

  auto z_score = measures::z_score(combined_points, measure_info);
  auto vacuumed_z_score = measures::vacuumed_z_score(combined_points);

  json output;

  output["z_score"] = z_score;
  output["vacuumed_z_score"] = vacuumed_z_score;
  output["seed"] = settings.seed;
  auto json_points = json::array();

  for (auto &&cluster : clusters) {
    for (auto &&point : cluster.points) {
      json row;
      row["x"] = point.x;
      row["y"] = point.y;
      row["point_id"] = boost::uuids::to_string(point.uuid);
      row["cluster_id"] = boost::uuids::to_string(cluster.uuid);
      row["centroid_x"] = cluster.centroid.x;
      row["centroid_y"] = cluster.centroid.y;
      json_points.push_back(row);
    }
  }

  output["points"] = json_points;

  return output;
}

void generate(Settings &settings) {

  // Set the seed and use the new seed (if 0) for Settings
  settings.seed = set_seed(settings.seed);

  std::vector<Point> centroids = make_centroids(settings);
  std::vector<Cluster> clusters;
  for (const Point &centroid : centroids) {
    Cluster cluster = Cluster::make_from_centroid(centroid, settings, clusters);
    clusters.push_back(std::move(cluster));
  }
  std::cout << make_json(clusters, settings) << "\n";
}
