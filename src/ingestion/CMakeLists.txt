cmake_minimum_required(VERSION 3.22)
project(phalanx_ingestion CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Discover foundational Protobuf and gRPC development packages
find_package(Protobuf REQUIRED)
find_package(gRPC REQUIRED)

# Paths for generated proto structures
set(PROTO_SRC_DIR "${CMAKE_CURRENT_SOURCE_DIR}/../../proto")
set(GEN_OUT_DIR "${CMAKE_CURRENT_BINARY_DIR}/generated")
file(MAKE_DIRECTORY ${GEN_OUT_DIR})

# Automatically compile proto targets during make cycle
add_custom_command(
    OUTPUT "${GEN_OUT_DIR}/telemetry.pb.cc" "${GEN_OUT_DIR}/telemetry.pb.h"
           "${GEN_OUT_DIR}/telemetry.grpc.pb.cc" "${GEN_OUT_DIR}/telemetry.grpc.pb.h"
    COMMAND ${PROTOBUF_PROTOC_EXECUTABLE}
    ARGS -I=${PROTO_SRC_DIR}
         --cpp_out=${GEN_OUT_DIR}
         --grpc_out=${GEN_OUT_DIR}
         --plugin=protoc-gen-grpc=$<TARGET_FILE:gRPC::grpc_cpp_plugin>
         "${PROTO_SRC_DIR}/telemetry.proto"
    DEPENDS "${PROTO_SRC_DIR}/telemetry.proto"
)

add_executable(phalanx_ingest 
    main.cpp 
    parser.hpp
    "${GEN_OUT_DIR}/telemetry.pb.cc"
    "${GEN_OUT_DIR}/telemetry.grpc.pb.cc"
)

target_include_directories(phalanx_ingest PRIVATE ${GEN_OUT_DIR} ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(phalanx_ingest PRIVATE gRPC::grpc++ protobuf::libprotobuf)
