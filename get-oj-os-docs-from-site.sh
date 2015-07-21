#! /bin/bash
[ $# -lt 1 ] && echo "please specify release number" && exit 1
rel=$1
mkdir ojuba-linux-docs 2>/dev/null || :
mkdir ojuba-linux-docs/images 2>/dev/null || :
mkdir release-notes 2>/dev/null || :
mkdir release-notes/images 2>/dev/null || :
pushd ojuba-linux-docs || {
  echo "can't change dir"
  exit 1
}
baseurl="http://www.ojuba.org/wiki/_export/xhtml/linux/"
imgbaseurl="http://www.ojuba.org/wiki/_media/linux/"

curl -L -o pg-list.htm "http://www.ojuba.org/wiki/tag/oj?do=showtag&tag=oj+oj${rel}"
perl -MURI::Escape -lwne 'if (m:\Q<td class="page"><ul><li><a href="/wiki/linux/\E([^"]*)\Q" class="wikilink1" title="\E[^"]*\Q">\E([^<>]*)\Q</a></li></ul></td>\E:) {print uri_unescape($1),":$2"}' pg-list.htm > pg-list.txt.in
grep -v 'الحصول_على_أعجوبة' pg-list.txt.in > pg-list.txt
rm pg-list.txt.in
cat ../tmp1.html >index.html

while read l
do
fn="${l/:*/}"
url="${baseurl}$fn"
t="${l/*:/}"
echo "$url"
echo "<li><a href='$fn.html'>$t</a></li>" >>index.html
curl -L -o "$fn.html" "$url"
perl -MURI::Escape -lwne 'for $i (m%src="/wiki/_media/linux/([^?"]+)(?:\?[^"]*)?"%g) {print uri_unescape($i)}' "$fn.html" > img-list-$fn.txt

perl -i -lwne 'BEGIN{$echo=1;}
s:href="/wiki/linux/([^"]+)":href="${1}.html":g;
s:src="/wiki/_media/linux/([^?"]+)(\?[^"]*)?":src="images/$1":g;
s:href="/wiki/_detail/linux/([^?"]+)(\?[^"]*)?":href="images/$1":g;
s!a href="http://!a target="_blank" href="http://!g;
s!a href="https://!a target="_blank" href="https://!g;
s:\Q<title>\E.*\Q</title>\E:<title>'"$t"'</title>:g;
if(/\<head[^>]*\>/){$echo=0;}
if(/#discussion__section|\<(link|meta|script)[^>]*\>/){next;}if (/class="tags"/) {$echo=0;}
if($echo){print $_;}if (/\<\/div\>/) {$echo=1;}

if(/\<\/head\>/) {
 print "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />";
 print "<link rel=\"stylesheet\" media=\"all\" type=\"text/css\" href=\"all.css\" />";
 print "<link rel=\"stylesheet\" media=\"screen\" type=\"text/css\" href=\"screen.css\" />";
 print "<link rel=\"stylesheet\" media=\"print\" type=\"text/css\" href=\"print.css\" />";
 $echo=1;
}
' "$fn.html"

done < pg-list.txt

cat ../tmp2.html >>index.html

echo "downloading images ..."
cat img-list-*.txt > img-list.txt
while read l
do
curl -L -o "images/$l" "${imgbaseurl}${l}"
done < img-list.txt

mv "ملحوظات-الإصدار-${rel}.html" ../release-notes/RELEASE-NOTES-ar.html
ln -s /usr/share/doc/HTML/release-notes/RELEASE-NOTES-ar.html "ملحوظات-الإصدار-${rel}.html" 

while read l
do
mv "images/$l" "../release-notes/images/$l"
ln -s "/usr/share/doc/HTML/release-notes/images/$l" "images/$l"
done < "img-list-ملحوظات-الإصدار-${rel}.txt"

rm pg-list.htm pg-list.txt img-list.txt img-list-*.txt

echo "done"

popd

