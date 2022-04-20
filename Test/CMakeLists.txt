cmake_minimum_required(VERSION 3.0.0)
project(testCpp VERSION 0.1.0)

# 设置指定的C++编译器版本是必须的，如果不设置，或者为OFF，则指定版本不可用时，会使用上一版本。
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 指定为C++11 版本
set(CMAKE_CXX_STANDARD 11)

include(CTest)
enable_testing()


include_directories(${CMAKE_CURRENT_LIST_DIR}/include)
include_directories(${CMAKE_CURRENT_LIST_DIR}/dto)

# 查找当前目录下的所有源文件
# 并将名称保存到 DIR_SRCS 变量
aux_source_directory(${CMAKE_CURRENT_LIST_DIR}/src DIR_SRCS)
aux_source_directory(${CMAKE_CURRENT_LIST_DIR}/dto DIR_SRCS)

add_executable(testCpp ${DIR_SRCS})

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
