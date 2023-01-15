#
# check that all the html files are valid xml
# sudo apt install libxml2-utils
# no output = pass
# zzz 1/23
#
for i in `find -name *.html`
do
	xmllint $i > /dev/null || echo "FAIL $i"
done
