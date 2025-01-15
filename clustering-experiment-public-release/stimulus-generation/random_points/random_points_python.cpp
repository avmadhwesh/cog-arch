#include "Point.hpp"
#include "measures.hpp"
#include "rand_utils.hpp"
#include "random_points_logic.hpp"
#include <boost/uuid/uuid_io.hpp>
#include <optional>
#include <pybind11/stl.h>
#include <vector>

namespace py = pybind11;

// if seed is 0, then regenerate a random one.
py::dict make_points(int n_points, unsigned int seed) {
  seed = set_seed(seed);
  auto points = generate_points(n_points);
  auto z_score = measures::z_score(
      points, measures::MeasureInformation{.n_points = n_points,
                                           .canvas_width = CANVAS_WIDTH,
                                           .canvas_height = CANVAS_HEIGHT});
  auto vacuumed_z_score = measures::vacuumed_z_score(points);

  py::dict output;
  output["z_score"] = z_score;
  output["vacuumed_z_score"] = vacuumed_z_score;
  output["seed"] = seed;
  output["base_uuid"] = boost::uuids::to_string(uuid_generator());

  py::list point_list;

  for (auto &&point : points) {
    py::dict py_point;
    py_point["x"] = point.x;
    py_point["y"] = point.y;
    point_list.append(py_point);
  }

  output["points"] = point_list;

  return output;
}

PYBIND11_MODULE(py_random_points, m) {
  m.doc() = "Generates random points.";

  m.def("make_points", &make_points,
        "Generates a stimulus with the required numbers of points.",
        py::arg("n_points"), py::arg("seed") = 0);
}
