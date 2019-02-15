#!/bin/bash
# Shell script to run the Dart GUI for user study.

# Run the flask server.
pipenv run python data_pass.py &

# Host the interface
URL="$PWD/interface/build/index.html"
if which xdg-open > /dev/null
then
  echo "xdg"
  xdg-open "$URL"
elif which gnome-open > /dev/null
then
    echo "gnome"
  gnome-open "$URL"
fi
