#! /bin/bash
mkdir ojuba-docs 2>/dev/null || :
mkdir ojuba-docs/images 2>/dev/null || :
pushd ojuba-docs || {
  echo "can't change dir"
  exit 1
}
baseurl="http://www.ojuba.org/wiki/_export/xhtml/docs/"
imgbaseurl="http://www.ojuba.org/wiki/_media/docs/"

curl -L -o pg-list.htm "${baseurl}/الصفحة_الأولى"
perl -MURI::Escape -lwne 'if (m:\Q<td class="page"><a href="/wiki/docs/\E([^"]*)\Q" class="wikilink1" title="\E[^"]*\Q">\E([^<>]*)\Q</a></td>\E:) {print uri_unescape($1),":$2"}' pg-list.htm > pg-list.txt

touch img-list.txt
rm img-list.txt
cat ../tmp1.html >index.html
while read l
do
fn="${l/:*/}"
url="${baseurl}$fn"
t="${l/*:/}"
echo "$url"
curl -L -o "$fn.html" "$url"
echo "<li><a href='$fn.html'>$t</a></li>" >>index.html
perl -MURI::Escape -lwne 'for $i (m%src="/wiki/_media/docs/([^?"]+)(?:\?[^"]*)?"%g) {print uri_unescape($i)}' "$fn.html" >> img-list.txt

perl -i -lwne 'BEGIN{$echo=1;}
s:href="/wiki/docs/([^"]+)":href="${1}.html":g;
s:src="/wiki/_media/docs/([^?"]+)(\?[^"]*)?":src="images/$1":g;
s:href="/wiki/_detail/docs/([^?"]+)(\?[^"]*)?":href="images/$1":g;
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

while read l
do
curl -L -o "images/$l" "${imgbaseurl}${l}"
done < img-list.txt

rm pg-list.htm pg-list.txt img-list.txt

echo "done"

popd

