#include "Settings.hpp"
#include "generate.hpp"
#include "json.hpp"
#include <iostream>
#include <string>

using json = nlohmann::json;

int main(int argc, char *argv[]) {
  auto j = json::parse(argv[1]);
  auto standard_deviation = j["standardDeviation"].get<double>();
  auto n_clusters = j["nClusters"].get<int>();
  auto points_per_cluster = j["pointsPerCluster"].get<int>();
  auto min_point_distance = j["minPointDistance"].get<int>();
  auto canvas_width = j["canvasWidth"].get<int>();
  auto canvas_height = j["canvasHeight"].get<int>();
  auto canvas_padding = j["canvasPadding"].get<int>();
  unsigned int seed = 0;
  try {
    seed = j["seed"].get<unsigned int>();
  } catch (json::type_error &e) {
    // do nothing cause seed is 0 by default
  }

  Settings settings{.standard_deviation = standard_deviation,
                    .n_clusters = n_clusters,
                    .points_per_cluster = points_per_cluster,
                    .min_point_distance = min_point_distance,
                    .canvas_width = canvas_width,
                    .canvas_height = canvas_height,
                    .canvas_padding = canvas_padding,
                    .seed = seed};

  generate(settings);
}
