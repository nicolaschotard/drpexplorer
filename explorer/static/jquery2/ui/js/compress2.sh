#!/bin/sh
cat jquery-ui-1.8.9.custom.min.js > ui.min.js
cat jquery.ui.selectmenu.js jquery.multiselect.js | slimit -m >> ui.min.js
