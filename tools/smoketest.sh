#!/bin/bash

DISTRONODE=$(pipdeptree --reverse -p distronode)

if [ -z "$DISTRONODE" ]; then
    echo "Distronode dependency not detected."
else
    echo "FATAL: Detected unexpected dependency on Distronode package"
    echo "$DISTRONODE"
    exit 2
fi
