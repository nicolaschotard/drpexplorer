#!/bin/sh
cat jquery-ui-1.8.9.custom.min.js jquery.ui.selectmenu.js jquery.multiselect.js > ui.js
java -jar ~/software/yuicompressor-2.4.2/build/yuicompressor-2.4.2.jar ui.js > ui.min.js
rm -f ui.js
