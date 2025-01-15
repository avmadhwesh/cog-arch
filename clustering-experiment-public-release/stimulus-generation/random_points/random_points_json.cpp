#include "Point.hpp"
#include "json.hpp"
#include "measures.hpp"
#include "rand_utils.hpp"
#include "random_points_logic.hpp"
#include <iostream>
#include <vector>

using json = nlohmann::json;

void print_json(std::vector<Point> points, double z_score,
                double vacuumed_z_score, unsigned int seed) {
  // Output
  json output;
  output["z_score"] = z_score;
  output["vacuumed_z_score"] = vacuumed_z_score;
  output["points"] = json::array();
  output["seed"] = seed;

  for (auto &&point : points) {
    json json_point;
    json_point["x"] = point.x;
    json_point["y"] = point.y;
    output["points"].push_back(json_point);
  }
  std::cout << output << "\n";
};

int main(int argc, char *argv[]) {
  auto j = json::parse(argv[1]);
  auto n_points = j["nPoints"].get<int>();
  unsigned int seed = 0;
  try {
    seed = j["seed"].get<unsigned int>();
  } catch (json::type_error &e) {
    // do nothing cause seed is 0 by default
  }

  // To set the randomization seed, and get the new one (if 0)
  seed = set_seed(seed);

  auto points = generate_points(n_points);
  auto z_score = measures::z_score(
      points, measures::MeasureInformation{.n_points = n_points,
                                           .canvas_width = CANVAS_WIDTH,
                                           .canvas_height = CANVAS_HEIGHT});
  auto vacuumed_z_score = measures::vacuumed_z_score(points);
  print_json(points, z_score, vacuumed_z_score, seed);
}
