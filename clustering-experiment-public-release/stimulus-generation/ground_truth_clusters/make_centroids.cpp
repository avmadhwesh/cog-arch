#include "Point.hpp"
#include "Settings.hpp"
#include <vector>

std::vector<Point> make_centroids(Settings const &settings) {

  auto standard_deviation = settings.standard_deviation;
  auto n_clusters = settings.n_clusters;
  auto canvas_width = settings.canvas_width;
  auto canvas_height = settings.canvas_height;
  auto canvas_padding = settings.canvas_padding;

  // Mini canvas is the part of the canvas excluding the padding. We'll
  // generate centroids in this mini canvas, and add the padding so that
  // the values match up with the real canvas.
  auto mini_canvas_width = canvas_width - 2 * canvas_padding;
  auto mini_canvas_height = canvas_height - 2 * canvas_padding;

  std::vector<Point> centroids;

  // Place the centroids into the mini canvas.
  centroids.push_back(Point::rand(mini_canvas_width, mini_canvas_height));
  while (centroids.size() != n_clusters) {
    Point candidate = Point::rand(mini_canvas_width, mini_canvas_height);
    auto too_close = false;
    for (Point &cpoint : centroids) {
      auto dist = cpoint.distance_to(candidate);
      if (dist <= standard_deviation) {
        too_close = true;
        break;
      }
    }

    if (!too_close) {
      centroids.push_back(candidate);
    }
  }

  // Now change the centroid values for the large canvas.
  for (Point &centroid : centroids) {
    centroid.x += canvas_padding;
    centroid.y += canvas_padding;
  }

  return centroids;
}
