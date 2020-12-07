#!/bin/bash

# convert all gerber files in this directory to pngs with 600 DPI

for f in *.ger
do
    echo "Processing $f"
    gerbv $f -x png -o $f.png -D 600 -a -b#FFFFFF -f#000000FF
done

for f in *.xln
do
    echo "Processing $f"
    gerbv $f -x png -o $f.png -D 600 -a -b#FFFFFF -f#000000FF
done


