#!/bin/sh
qstat -u `whoami` | grep "h" | grep "_"