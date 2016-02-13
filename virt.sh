#!/bin/bash
if [[ "${BASH_SOURCE[0]}" != "${0}" ]] ; then
    path=~/.virtualenv/dbdiff/bin/activate
    echo "sourcing virtualenv at $path"
    source $path
else
    echo "Must source this script!"
    exit 255
fi
