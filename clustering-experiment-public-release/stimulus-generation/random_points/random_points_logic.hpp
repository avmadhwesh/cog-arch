#pragma once
#include "Point.hpp"
#include <vector>

const int MIN_POINT_DISTANCE = 12;
const int CANVAS_WIDTH = 800;
const int CANVAS_HEIGHT = 500;
const int CANVAS_MARGIN = 7;

std::vector<Point> generate_points(int n_points);
