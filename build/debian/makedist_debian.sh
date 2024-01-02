#!/usr/bin/env bash
set -x # print all commands
set -e # exit when any command fails

LOG_LEVEL=${LOG_LEVEL:-"DEBUG"}

if [[ ! -d build/debian ]]; then
  echo "Please run this script from project root as:\n./build/debian/makedist_debian.sh"
fi

rm -rf build/tribler
rm -rf dist/tribler
rm -rf build/debian/tribler/usr/share/tribler

if [ ! -z "$VENV" ]; then
  echo "Setting venv to $VENV"
  source $VENV/bin/activate
else
  echo "Creating a new venv"
  python3 -m venv build-env
  . ./build-env/bin/activate
fi

# ----- Install dependencies before the build
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade -r requirements.txt

# ----- Build binaries
python3 -m PyInstaller pyinstaller.spec --log-level="${LOG_LEVEL}"

# ----- Build dpkg
cp -r ./dist/tribler ./build/debian/tribler/usr/share/tribler

TRIBLER_VERSION='10.0.0'

# Compose the changelog
cd ./build/debian/tribler

dch -v $TRIBLER_VERSION "New release"
dch -v $TRIBLER_VERSION "See https://github.com/Tribler/tribler/releases/tag/$TRIBLER_VERSION for more info"

dpkg-buildpackage -b -rfakeroot -us -uc
