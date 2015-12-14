#!/bin/bash

roslaunch mavros apm.launch fcu_url:=$1 gcs_url:=udp://@
