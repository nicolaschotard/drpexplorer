var cache, current_tab, data, globals, openTab, plots;
var __indexOf = Array.prototype.indexOf || function(item) {
  for (var i = 0, l = this.length; i < l; i++) {
    if (this[i] === item) return i;
  }
  return -1;
};
globals = window;
globals.tabs = [];
globals.openthislc = null;
globals.current_spec_exp = null;
globals.previousPoint = null;
cache = [];
current_tab = null;
plots = {};
data = {};
openTab = function(tab) {
  current_tab = tab;
  if (__indexOf.call(cache, tab) < 0) {
    cache.push(tab);
    switch (tab) {
      case 'DRP':
        break;
    }
  }
};
$(function() {
  var t;
  $('#tabs').tabs({
    cache: true,
    ajaxOptions: {
      async: false
    },
    add: function(event, ui) {
      return globals.tabs.push(ui.panel.id);
    },
    show: function(event, ui) {
      return openTab(ui.panel.id);
    }
  });
  $(".ui-widget-content:not(.ui-tabs):not(.ui-helper-clearfix)").addClass('ui-helper-clearfix');
  globals.tabs = (function() {
    var _i, _len, _ref, _results;
    _ref = $('[tab]');
    _results = [];
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      t = _ref[_i];
      _results.push($(t).attr('href').replace('#', ''));
    }
    return _results;
  })();
  openTab(tabs[$('#tabs').tabs('option', 'selected')]);
  $(document).bind('keydown', function(event) {
    return window.currentKey = event.keyCode;
  });
  $(document).bind('keyup', function(event) {
    return window.currentKey = null;
  });
  return true;
});
