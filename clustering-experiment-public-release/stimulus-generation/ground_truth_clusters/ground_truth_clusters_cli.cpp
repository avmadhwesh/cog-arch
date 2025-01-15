#include "Cluster.hpp"
#include "Point.hpp"
#include "Settings.hpp"
#include "args.hxx"
#include "generate.hpp"
#include "make_centroids.hpp"
#include "measures.hpp"
#include "rand_utils.hpp"
#include <iostream>
#include <sstream>
#include <vector>

// Debugging tool
/* template <class T> void print(T thing) { std::cout << thing << "\n"; } */

int main(int argc, char *argv[]) {
  args::ArgumentParser parser("Vijay's Item Generator");

  args::ValueFlag<double> standard_deviation(
      parser, "standard-deviation", "Standard deviation for centroid spacing",
      {"standard-deviation"}, args::Options::Required);

  args::ValueFlag<int> n_clusters(parser, "n-clusters", "Number of clusters",
                                  {"n-clusters"}, args::Options::Required);

  args::ValueFlag<int> points_per_cluster(parser, "ppc", "Points per cluster",
                                          {"points-per-cluster"},
                                          args::Options::Required);
  args::ValueFlag<int> min_point_distance(
      parser, "min-point-distance", "Minimum point distance",
      {"min-point-distance"}, args::Options::Required);

  args::ValueFlag<int> canvas_width(parser, "canvas-width",
                                    "Width of the canvas", {"canvas-width"},
                                    args::Options::Required);

  args::ValueFlag<int> canvas_height(parser, "canvas-height",
                                     "Height of the canvas", {"canvas-height"},
                                     args::Options::Required);

  args::ValueFlag<int> canvas_padding(
      parser, "canvas-padding", "Padding within canvas", {"canvas-padding"},
      args::Options::Required);

  args::ValueFlag<unsigned int> seed(parser, "seed", "Randomization seed",
                                     {"seed"}, 0);

  args::HelpFlag help(parser, "help", "Display this help menu", {'h', "help"});

  try {
    parser.ParseCLI(argc, argv);
  } catch (args::Help) {
    std::cout << parser;
    return 0;
  }

  Settings settings{.standard_deviation = args::get(standard_deviation),
                    .n_clusters = args::get(n_clusters),
                    .points_per_cluster = args::get(points_per_cluster),
                    .min_point_distance = args::get(min_point_distance),
                    .canvas_width = args::get(canvas_width),
                    .canvas_height = args::get(canvas_height),
                    .canvas_padding = args::get(canvas_padding),
                    .seed = args::get(seed)};

  generate(settings);
}
