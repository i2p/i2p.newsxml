#! /usr/bin/env sh
# This script is used to download and extract the latest news from I2P
# and display it on a terminal. I use it to test when I check in the news.
i2p() {
    java -jar ~/i2p/lib/i2p.jar "$@"
}

if [ ! -f news.su3 ]; then
    echo "Downloading news.su3..."
    eepget http://tc73n4kivdroccekirco7rhgxdg5f3cjvbaapabupeyzrqwv5guq.b32.i2p/news.su3
fi
i2p su3file extract -x news.su3
gunzip news.xml.gz
less news.xml 