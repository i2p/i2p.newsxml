#! /usr/bin/env sh
dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

if [ grep darwin "$OSTYPE" > /dev/null ]; then
    echo "Running on macOS, using greadlink to resolve path"
    I2PHOME="$HOME/Library/Application Support/i2p"
else
    I2PHOME="$HOME/i2p/"
fi

echo "Changing to xml working dir: $dir"
cd "$dir" || exit 1
echo "Removing old backup build directory"
rm "$dir/build.old" -rf
echo "Moving build directory to build.old"
mv "$dir/build" "$dir/build.old"
echo "Building signing container i2p.newsxml"
docker build -t i2p.newsxml.signing -f Dockerfile.signing .
echo "Removing old signing container"
docker rm -f i2p.newsxml.signing
echo "Running signing container"
docker run -it \
    -u $(id -u):$(id -g) \
    --name i2p.newsxml.signing \
    -v $HOME/.i2p-plugin-keys/:/.i2p-plugin-keys/:ro \
    -v $I2PHOME:/i2p/:ro \
    i2p.newsxml.signing
docker cp i2p.newsxml.signing:/opt/i2p.newsxml/build build