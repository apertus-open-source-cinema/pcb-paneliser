#!/bin/bash

mkdir jlcpcb

# *.xln -> *.drd
for f in *.drills.xln; do 
    cp -- "$f" "jlcpcb/${f%.drills.xln}.drd"
done

# *.toplayer.ger -> *.GTL
for f in *.toplayer.ger; do 
    cp -- "$f" "jlcpcb/${f%.toplayer.ger}.GTL"
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

# *.internalplane1.ger -> *.G2L
for f in *.internalplane1.ger; do 
    cp -- "$f" "jlcpcb/${f%.internalplane1.ger}.G2L"
done

# *.internalplane2.ger -> *.G3L
for f in *.internalplane2.ger; do 
    cp -- "$f" "jlcpcb/${f%.internalplane2.ger}.G3L"
done

# *.bottomlayer.ger -> *.GBL
for f in *.bottomlayer.ger; do 
    cp -- "$f" "jlcpcb/${f%.bottomlayer.ger}.GBL"
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

# *.boardoutline.ger -> *.GKO
for f in *.boardoutline.ger; do 
    cp -- "$f" "jlcpcb/${f%.boardoutline.ger}.GKO"
done

