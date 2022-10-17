#!/bin/bash

set -e

exec python capture.py &
exec python toVideo.py
