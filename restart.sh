#!/bin/bash

`sudo service supervisor stop`
`sudo service uwsgi stop`
`sudo service nginx stop`
`sudo service nginx start`
`sudo service uwsgi start`
`sudo service supervisor start`
