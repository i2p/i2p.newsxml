#! /usr/bin/env sh
dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
echo "Changing to xml working dir: $dir"
cd "$dir" || exit 1

if [ -f "etc/su3.vars" ]; then
    . etc/su3.vars
fi
if [ -f "etc/su3.vars.custom" ]; then
    . etc/su3.vars.custom
fi
if [ -f "etc/su3.vars.custom.docker" ]; then
    . etc/su3.vars.custom.docker
fi


if [ -d "$dir/build" ]; then
    echo "Building hosting container i2p.newsxml"
    docker build -t i2p.newsxml .
    echo "Removing old newsxml container"
    docker rm -f newsxml
    echo "Running newsxml container"
    docker run -d --restart=always --name newsxml -p 127.0.0.1:"$SERVEPORT":3000 i2p.newsxml
else 
    echo "No build directory found. Perform the signing procedure with news.sh or docker-news.sh."
    exit 1
fi