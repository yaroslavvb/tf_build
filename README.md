# Automatically launching TensorFlow build on Amazon

This is a script to reserve a `p3.16xlarge` instance, configure environment for CUDA 9.0/CuDNN 7.0 and start the build process of latest TensorFlow version

You need the following:

- select region with P3 instances one of IAD/PDX/Dublin (ie `us-west-2`)
- a security group that allows SSH access (ie, `open`)
- SSH keyname/.pem pair (ie, `yaroslav` and `~/yaroslav.pem`)
- Local Python 3.5+ installation with pip configured

Once you have these things, configure your environment

```
export AWS_DEFAULT_REGION=us-west-2
export SECURITY_GROUP=open
export KEY_NAME=yaroslav
export SSH_KEY_PATH=yaroslav.pem
aws configure
```

Now launch the build as follows

```
pip install -r requirements.txt
tf_build.py
```

To connect to the instance and observe the progress

```
./connect
tmux a
```

Note that `connect` connects to the most recently launched instance, if you have multiple instances, look inside `connect` for instructions how to select an instance

At the end of build, the script writes to `/tmp/is_initialized` file on the instance. If you restart the script, it will skip steps in `INSTALL_SCRIPT` if this file is present, so if you want to start over, make sure to delete this file on the instance.

Once you are done with your instances, shut them down using terminate script

```
terminate
```