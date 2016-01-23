#!/bin/sh

BUILD=./build
NEWS_PREFIX=$BUILD/news_
ATOM_SUFFIX=.atom.xml

. ./etc/su3.vars
[ -f ./etc/su3.vars.custom ] && . ./etc/su3.vars.custom

echo "Enter password for signer $SIGNER in keystore $KS:"
read password

./generate_news.py
echo "$password" | ./make-su3-news.sh $BUILD/news.atom.xml $BUILD/news.su3
for file in `ls $NEWS_PREFIX*$ATOM_SUFFIX`; do
    lang=$(expr substr $file $(expr $(expr length $NEWS_PREFIX) + 1) $(expr $(expr length $file) - $(expr length $NEWS_PREFIX) - $(expr length $ATOM_SUFFIX)))
    echo "$password" | ./make-su3-news.sh $file $NEWS_PREFIX$lang.su3
done
