#!/bin/bash

# Stuart's build script. Yes.
# Basically this is here to confirm that Stuart remembered to update the version in both files

PYV=$(grep "version =" pyproject.toml | cut -d'"' -f2)
SNAPV=$(grep '^version:' snapcraft.yaml | cut -d'"' -f2)

if [ A$PYV != A$SNAPV ]; then
    echo The versions from snapcraft.yaml and pyproject.toml differ. Fix it.
    exit 1
fi

echo Building version $SNAPV as snap
snapcraft --debug


