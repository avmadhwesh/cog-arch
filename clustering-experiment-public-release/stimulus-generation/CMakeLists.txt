cmake_minimum_required(VERSION 3.15)

project(PointGenerator)

find_package(Boost REQUIRED) # for uuid
add_subdirectory(deps/pybind11) # for python binding

set(GENERAL_DEPS general/Point.cpp general/rand_utils.cpp general/measures.cpp)
set(GROUND_TRUTH_CLUSTERS_DEPS
    ground_truth_clusters/Cluster.cpp ground_truth_clusters/make_centroids.cpp
    ground_truth_clusters/generate.cpp)
set(RANDOM_POINTS_DEPS random_points/random_points_logic.cpp)

add_executable(
  ground-truth-clusters-cli ground_truth_clusters/ground_truth_clusters_cli.cpp
                            ${GENERAL_DEPS} ${GROUND_TRUTH_CLUSTERS_DEPS})
target_link_libraries(ground-truth-clusters-cli -static)
set_property(TARGET ground-truth-clusters-cli PROPERTY CXX_STANDARD 17)
target_include_directories(
  ground-truth-clusters-cli PRIVATE deps/json deps/args general
                                    ${BOOST_INCLUDE_DIRS})

add_executable(
  ground-truth-clusters-json
  ground_truth_clusters/ground_truth_clusters_json.cpp ${GENERAL_DEPS}
  ${GROUND_TRUTH_CLUSTERS_DEPS})
target_link_libraries(ground-truth-clusters-json -static)
set_property(TARGET ground-truth-clusters-json PROPERTY CXX_STANDARD 17)
target_include_directories(ground-truth-clusters-json
                           PRIVATE deps/json general ${BOOST_INCLUDE_DIRS})

add_executable(random-points-json random_points/random_points_json.cpp
                                  ${GENERAL_DEPS} ${RANDOM_POINTS_DEPS})
target_link_libraries(random-points-json -static)
set_property(TARGET random-points-json PROPERTY CXX_STANDARD 17)
target_include_directories(random-points-json PRIVATE deps/json general
                                                      ${BOOST_INCLUDE_DIRS})

set(PYBIND11_CPP_STANDARD -std=c++17)
pybind11_add_module(py_random_points random_points/random_points_python.cpp
                    ${GENERAL_DEPS} ${RANDOM_POINTS_DEPS})
target_include_directories(py_random_points PRIVATE deps general
                                                    ${BOOST_INCLUDE_DIRS})
