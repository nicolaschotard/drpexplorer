#!/bin/sh
cat jquery-1.6.1.min.js > all.min.js
cat ../flot/jquery.flot.js ../flot/jquery.flot.crosshair.js ../flot/jquery.flot.axislabels.js \
../flot/jquery.flot.errorbars.js ../flot/jquery.flot.fillbetween.js ../flot/jquery.flot.navigate.js \
../flot/jquery.flot.selection.js ../flot/jquery.flot.stack.js ../flot/jquery.flot.symbol.js \
../flot/jquery.flot.text.js jquery.jsanalysis.js | slimit >> all.min.js
