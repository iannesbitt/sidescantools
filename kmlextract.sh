for f in *.DAT; do
  filename=$(basename "$f")
  dn="${filename%.*}"
  for dir in $dn/; do
    cp "$dn"/"$dn""trackline.kml" ./
  done
done
