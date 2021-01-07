mkdir output_rotated
for f in $1/*.ger;  
do echo ${f};
gerbv ${f} -x rs274x -umm -T0x0r270 -o output_rotated/${f##*/}
done;

for f in $1/*.xln; 
do echo ${f};
gerbv ${f} -x drill -umm -T0x0r270 -o output_rotated/${f##*/}
done;

mv $1 $1_original
mv output_rotated $1
