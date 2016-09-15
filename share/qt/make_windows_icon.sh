#!/bin/bash
# create multiresolution windows icon
ICON_SRC=../../src/qt/res/icons/gongxincoin.png
ICON_DST=../../src/qt/res/icons/gongxincoin.ico
convert ${ICON_SRC} -resize 16x16 gongxincoin-16.png
convert ${ICON_SRC} -resize 32x32 gongxincoin-32.png
convert ${ICON_SRC} -resize 48x48 gongxincoin-48.png
convert gongxincoin-16.png gongxincoin-32.png gongxincoin-48.png ${ICON_DST}

