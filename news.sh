#!/bin/sh

BUILD=./build/"$I2P_OS"/"$I2P_BRANCH"
RELEASES=./data/"$I2P_OS"/"$I2P_BRANCH"/releases.json
NEWS_PREFIX=$BUILD/news_
ATOM_SUFFIX=.atom.xml
TMP=$BUILD/tmp
TMP_PREFIX=$TMP/news_
XML_GZ_SUFFIX=.xml.gz
SU3_SUFFIX=.su3

. ./etc/su3.vars
[ -f ./etc/su3.vars.custom ] && . ./etc/su3.vars.custom

verify_xml () {
    local in="$1"

    # Verify it is valid XML using our parser
    java -cp $I2P/lib/i2p.jar:$I2P/lib/router.jar:$I2P/lib/routerconsole.jar net.i2p.router.news.NewsXMLParser $in
    if [ $? -ne 0 ]
    then
        echo "XML verification of $in failed"
        exit 1
    fi
    echo
}

prepare_lang_gz () {
    local file=$1

    verify_xml $file
    lang=$(expr substr $file $(expr $(expr length $NEWS_PREFIX) + 1) $(expr $(expr length $file) - $(expr length $NEWS_PREFIX) - $(expr length $ATOM_SUFFIX)))
    gzip -c -n $file > "$TMP_PREFIX$lang$XML_GZ_SUFFIX"
}

show_su3_and_mv () {
    local file=$1

    echo
    echo "$file:"
    java -cp $I2P/lib/i2p.jar net.i2p.crypto.SU3File \
        showversion $file
    mv $file $BUILD
}

final_generate_signed_feeds () {
    python3 ./generate_news.py
    sleep 20s

    mkdir -p $TMP

    verify_xml $BUILD/news.atom.xml
    gzip -c -n $BUILD/news.atom.xml > "$TMP/news$XML_GZ_SUFFIX"
    for file in `ls $NEWS_PREFIX*$ATOM_SUFFIX`; do
        prepare_lang_gz $file
    done

    NOW=`date +%s`
    java -cp $I2P/lib/i2p.jar net.i2p.crypto.SU3File \
        bulksign -c NEWS -f XML_GZ -t RSA_SHA512_4096 $TMP $KS $NOW $SIGNER

    if [ $? -ne 0 ]
    then
        echo "Failed to bulksign news files"
        exit 1
    fi

    show_su3_and_mv "$TMP/news$SU3_SUFFIX"
    for file in `ls $TMP_PREFIX*$SU3_SUFFIX`; do
        show_su3_and_mv $file
    done

    rm -r $TMP
    echo
    ls -l $BUILD
}

I2P_OSS="win mac"
I2P_BRANCHES="beta stable testing"

if [ -z $I2P_OS ]; then
  if [ -z $I2P_BRANCH ]; then
    for I2P_OS in $I2P_OSS; do
      for I2P_BRANCH in $I2P_BRANCHES; do
        echo "building news for: $I2P_OS, $I2P_BRANCH."
        export I2P_OS
        export I2P_BRANCH
        ./news.sh
      done
    done
  fi
else
  if [ -f $RELEASES ]; then
    final_generate_signed_feeds
  fi
fi

