#!/bin/bash

RED="\033[0;31m"
GREEN="\033[0;32m"
NC="\033[0m" # No Color

# Run migrations.
if ./manage.py migrate; then
    echo -e "${GREEN}Database migrated.${NC}"
else
    echo -e "${RED}Couldn't migrate the database.${NC}"
    exit 1
fi

# Kick off Django dev server.
./manage.py runserver 0.0.0.0:8000
