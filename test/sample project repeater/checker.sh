#!/bin/bash

read val

if [ $val -le 1 ]; then
    exit 1
fi
