#!/bin/bash

mkdir jlcpcb

# *.xln -> *.drd
for f in *.xln; do 
    cp -- "$f" "jlcpcb/${f%.xln}.drd"
done

# *.toplayer.ger -> *.cmp
for f in *.toplayer.ger; do 
    cp -- "$f" "jlcpcb/${f%.toplayer.ger}.cmp"
done

# *.topsoldermask.ger -> *.stc
for f in *.topsoldermask.ger; do 
    cp -- "$f" "jlcpcb/${f%.topsoldermask.ger}.stc"
done

# *.topcream.ger -> *.crc
for f in *.topcream.ger; do 
    cp -- "$f" "jlcpcb/${f%.topcream.ger}.crc"
done

# *.topsilkscreen.ger -> *.plc
for f in *.topsilkscreen.ger; do 
    cp -- "$f" "jlcpcb/${f%.topsilkscreen.ger}.plc"
done

# *.internalplane1.ger -> *.ly2
for f in *.internalplane1.ger; do 
    cp -- "$f" "jlcpcb/${f%.internalplane1.ger}.ly2"
done

# *.internalplane2.ger -> *.l15
for f in *.internalplane2.ger; do 
    cp -- "$f" "jlcpcb/${f%.internalplane2.ger}.l15"
done

# *.bottomlayer.ger -> *.sol
for f in *.bottomlayer.ger; do 
    cp -- "$f" "jlcpcb/${f%.bottomlayer.ger}.sol"
done

# *.bottomsoldermask.ger -> *.sts
for f in *.bottomsoldermask.ger; do 
    cp -- "$f" "jlcpcb/${f%.bottomsoldermask.ger}.sts"
done

# *.bottomcream.ger -> *.crs
for f in *.bottomcream.ger; do 
    cp -- "$f" "jlcpcb/${f%.bottomcream.ger}.crs"
done

# *.bottomsilkscreen.ger -> *.pls
for f in *.bottomsilkscreen.ger; do 
    cp -- "$f" "jlcpcb/${f%.bottomsilkscreen.ger}.pls"
done

# *.boardoutline.ger -> *.gko
for f in *.boardoutline.ger; do 
    cp -- "$f" "jlcpcb/${f%.boardoutline.ger}.gko"
done

