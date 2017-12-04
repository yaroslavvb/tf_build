#!/usr/bin/env python

# Launches P3.16xlarge instance with Amazon Ubuntu Deep Learning AMI,
# and launches TensorFlow CUDA 9.0 build on it.
#
# AMI URL is the following
# https://aws.amazon.com/marketplace/pp/B077GCH38C?qid=1512418106283&sr=0-2&ref_=srh_res_product_title
#
# Clones TensorFlow repo and follows the process in
# tensorflow/tensorflow/tools/docker/Dockerfile.devel-gpu

import os
import argparse

parser = argparse.ArgumentParser(description='p3')
parser.add_argument('--run', type=str, default='tf_build',
                     help="name of the current run")
parser.add_argument('--instance_type', type=str, default='p3.16xlarge',
                     help="type of instance")
parser.add_argument('--role', type=str, default='launcher',
                     help=('script role (launcher or worker)'))
args = parser.parse_args()

ami_dict = {
    "us-east-1": "ami-405ade3a",
    "us-east-2": "ami-f0725c95",
    "us-west-2": "ami-f1e73689",
    "eu-west-1": "ami-1812bb61",
    "ap-southeast-2": "ami-5603eb34",
    "ap-northeast-2": "ami-0ce14662",
    "ap-northeast-1": "ami-329c2b54",
}

LINUX_TYPE = "ubuntu"  # linux type determines username to use to login
INSTALL_SCRIPT="""
# larger history
tmux set-option -g history-limit 50000

# helper utilities
sudo apt update -y
sudo pip install paramiko
sudo apt install -y dtach
sudo apt install -y emacs24
sudo apt install -y expect
sudo apt install -y htop

# clone tensorflow repo and run install scripts
git clone https://github.com/tensorflow/tensorflow.git
cd tensorflow/tensorflow/tools/ci_build
export DEBIAN_FRONTEND=noninteractive

sudo install/install_bootstrap_deb_packages.sh
sudo add-apt-repository -y ppa:openjdk-r/ppa && sudo add-apt-repository -y ppa:george-edison55/cmake-3.x

# fixes to take into account the fact that python3 is installed by default
ln -s /home/ubuntu/anaconda3/bin/easy_install /home/ubuntu/anaconda3/bin/easy_install3
sudo rm -Rf /usr/local/bin/pip3
hash -r   # clear symlink cache
sudo install/install_pip_packages.sh
sudo install/install_bazel.sh
sudo install/install_golang.sh
sudo cp install/.bazelrc /etc/bazel.bazelrc

# take library path from python3 environment, replace with cuda 9
export LD_LIBRARY_PATH=/usr/local/cuda-9.0/lib64:/usr/local/cuda-9.0/extras/CUPTI/lib64:/lib/nccl/cuda-9:/usr/lib64/openmpi/lib/:/usr/local/lib:/usr/lib:/usr/local/mpi/lib:/lib/:/usr/lib64/openmpi/lib/:/usr/local/lib:/usr/lib:/usr/local/mpi/lib:/lib/:/usr/lib64/openmpi/lib/:/usr/local/lib:/usr/lib:/usr/local/mpi/lib:/lib/

# follow tensorflow/tensorflow/tools/docker/Dockerfile.devel-gpu
sudo apt-get update && sudo apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        git \
        libcurl3-dev \
        libfreetype6-dev \
        libpng12-dev \
        libzmq3-dev \
        pkg-config \
        python-dev \
        rsync \
        software-properties-common \
        unzip \
        zip \
        zlib1g-dev \
        openjdk-8-jdk \
        openjdk-8-jre-headless \
        wget \
        && \
    sudo apt-get clean && \
    sudo rm -rf /var/lib/apt/lists/*

sudo pip3 --no-cache-dir install \
        ipykernel \
        jupyter \
        matplotlib \
        numpy \
        scipy \
        sklearn \
        pandas

export CI_BUILD_PYTHON=python
sudo ln -s /usr/local/cuda/lib64/stubs/libcuda.so /usr/local/cuda/lib64/stubs/libcuda.so.1

pushd ~/tensorflow

# TF ./configured script was broken so use custom expect script 
wget https://gist.githubusercontent.com/yaroslavvb/691eded946738ffa4c84478c12898d46/raw/11b7d7d06a349bd63a74f0b6fa02626c66e0deef/configure_cuda9.sh
chmod 755 configure_cuda9.sh
./configure_cuda9.sh

bazel build -c opt --config=cuda --cxxopt="-D_GLIBCXX_USE_CXX11_ABI=0" tensorflow/tools/pip_package:build_pip_package
"""


def main():
  if args.role == 'launcher':
    assert "AWS_DEFAULT_REGION" in os.environ
    assert os.environ.get("AWS_DEFAULT_REGION") in ami_dict
    AMI = ami_dict[os.environ.get("AWS_DEFAULT_REGION")]
    
    import aws
    job = aws.simple_job(args.run, num_tasks=1,
                         instance_type=args.instance_type,
                         install_script=INSTALL_SCRIPT,
                         ami=AMI, linux_type=LINUX_TYPE)
    task = job.tasks[0]
    job.initialize()
    job.wait_until_ready()

    task.run('cd ~')
    task.upload(__file__)   # copies current script onto machine
    task.run("python %s --role=worker" % (__file__,)) # runs script and streams output locally to file in /temp
    print("To connect:")
    print(task.connect_instructions)
    
  elif args.role == 'worker':
    import sys, time
    print('Python version is '+str(sys.version))

if __name__=='__main__':
  main()
