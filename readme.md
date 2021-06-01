# Notes on the shared task

This repo has the relevant files to recreate our entry for the SIGMORPHON 2021 G2P shared task.

Everything was run using OpenNMT-py in a docker image.

## Configuring the docker image

Build an image like this:

```bash
docker run -it --gpus all --name nmtpy \
	-v ~/somefolder:/mh \
	pytorch/pytorch:1.7.0-cuda11.0-cudnn8-runtime
```

The `somefolder` should contain the `2021-task1-main` folder from the SIGMORPHON 2021 github repo.

Inside the image, install `opennmt-py` like this:

```bash
pip install OpenNMT-py
```

Some additional convenient stuff:

```bash
apt update
apt install vim
apt install wget
```

## Other files here

- `final.sh`: master batch file; this calls everything else.
- `big.yaml`: configuration file for OpenNMT, invoked by `final.sh`
- `mfinal.py`: data munging, called by `final.sh`
- `stats.py`: does the $t$-tests for the paper
- `wer.py`: does the Monte Carlo estimates of word-level accuracy

