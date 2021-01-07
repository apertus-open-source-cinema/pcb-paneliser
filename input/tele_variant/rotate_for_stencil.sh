mkdir output_rotated

for f in $1/*-mirrored.ger;  
do echo ${f};
gerbv ${f} -x rs274x -umm -T0x0r270 -o output_rotated/${f##*/}
done;

for f in $1/*boardoutline.ger;  
do echo ${f};
gerbv ${f} -x rs274x -umm -T0x0r90 -o output_rotated/${f##*/}
done;

for f in $1/*topcream.ger;  
do echo ${f};
gerbv ${f} -x rs274x -umm -T0x0r90 -o output_rotated/${f##*/}
done;


mv $1 $1_original
mv output_rotated $1
