#!/usr/bin/expect -d
# uploaded to https://gist.githubusercontent.com/yaroslavvb/691eded946738ffa4c84478c12898d46/raw/11b7d7d06a349bd63a74f0b6fa02626c66e0deef/configure_cuda9.sh
spawn ./configure

expect "Please specify the location of python"
send "\r"
expect "Please input the desired Python library path to use"
send "\r"
expect "Do you wish to build TensorFlow with jemalloc as malloc support?"
send "\r"
expect "Do you wish to build TensorFlow with Google Cloud Platform support?"
send "\r"
expect "Do you wish to build TensorFlow with Hadoop File System support?"
send "\r"
expect "Do you wish to build TensorFlow with Amazon S3 File System support?"
send "\r"
expect "Do you wish to build TensorFlow with XLA JIT support?"
send "\r"
expect "Do you wish to build TensorFlow with GDR support?"
send "\r"
expect "Do you wish to build TensorFlow with VERBS support?"
send "\r"
expect "Do you wish to build TensorFlow with OpenCL SYCL support?"
send "\r"
expect "Do you wish to build TensorFlow with CUDA support?"
send "y\r"
expect "Please specify the CUDA SDK version you want to use"
send "9.0\r"
expect "Please specify the location where CUDA 9.0 toolkit is installed"
send "/usr/local/cuda-9.0\r"
expect "Please specify the cuDNN version you want to use"
send "7\r"
expect "Please specify the location where"
send "/usr/local/cuda-9.0\r"
# this gets default 7.0, 7.0, 7.0 , etc
expect "Please specify a list of comma-separated Cuda compute capabilities"
send "\r"
expect "Do you want to use clang as CUDA compiler?"
send "\r"
expect "Please specify which gcc should be used by nvcc as the host compiler"
send "\r"
expect "Do you wish to build TensorFlow with MPI support?"
send "\r"
expect "Please specify optimization flags to use during compilation"
send "\r"

