#!/bin/bash
set -e

if [ "$SETUP_STATUS" = "production" ]; then
    /usr/local/bin/update_notebooks
fi

exec "$@"