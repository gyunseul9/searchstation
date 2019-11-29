#!/bin/bash

source /home/ubuntu/collector/bin/activate

exec uwsgi --ini /home/ubuntu/searchstation/env/uwsgi.ini --py-autoreload 1