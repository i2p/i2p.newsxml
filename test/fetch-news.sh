#
# pull and verify translated news
#
# usage: fetch-news.sh [xx[_XX]]
#
# zzz 2015-09-01
# public domain
#

I2P=$HOME/i2p
PROXY=localhost:4444

TMP1=/var/tmp/foo$$.su3
TMP2=/var/tmp/foo$$.xml.gz
TMP3=/var/tmp/foo$$.xml

# echelon
URL=http://tc73n4kivdroccekirco7rhgxdg5f3cjvbaapabupeyzrqwv5guq.b32.i2p/news.su3
SIGNER=echelon_at_mail.i2p
# psi
#URL=http://avviiexdngd32ccoy4kuckvc3mkf53ycvzbz6vz75vzhv4tbpk5a.b32.i2p/news.su3
#SIGNER=ampernand_at_gmail.com

if [ "$LANG" != "" ]
then
	LG=`echo $LANG | cut -f 1 -d '.'`
fi

echo "default language is $LG"

if [ $# -gt 0 ]
then
	LG=$1
fi

echo "requested language is $LG"

if [ "$LG" != "" ]
then
	URL="${URL}?lang=$LG"
fi

eepget -p $PROXY -o $TMP1 $URL

if [ $? -ne 0 ]
then
	echo "eepget failed"
	rm -f $TMP1
	exit 1
fi

java -cp ${I2P}/lib/i2p.jar -Djava.library.path=$I2P net.i2p.crypto.SU3File showversion $TMP1

if [ $? -ne 0 ]
then
	echo "showversion failed"
	rm -f $TMP1 $TMP2
	exit 1
fi

java -cp ${I2P}/lib/i2p.jar -Djava.library.path=$I2P net.i2p.crypto.SU3File -k ${I2P}/certificates/news/${SIGNER}.crt extract $TMP1 $TMP2

if [ $? -ne 0 ]
then
	echo "extract failed"
	rm -f $TMP1 $TMP2
	exit 1
fi

gunzip -c $TMP2 > $TMP3

if [ $? -ne 0 ]
then
	echo "gunzip failed"
	rm -f $TMP1 $TMP2 $TMP3
	exit 1
fi

echo
echo '========================================='

# Verify it is valid XML using our parser
java -cp $I2P/lib/i2p.jar:$I2P/lib/router.jar:$I2P/lib/routerconsole.jar net.i2p.router.news.NewsXMLParser $TMP3

if [ $? -ne 0 ]
then
	echo "XML verification failed"
	rm -f $TMP1 $TMP2 $TMP3
	exit 1
fi



echo '========================================='
echo PASSED
rm -f $TMP1 $TMP2 $TMP3
