#!/bin/bash

clear;

if ! [ -x "$(command -v pytest)" ]; then
    echo 'Error: pytest is not installed.' >&2
    exit 1;
fi

pytest --capture=sys;

exit;