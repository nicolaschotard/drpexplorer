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
$.getJSON('/preferences/', function(data) {
  return globals.preferences = data;
});
$(window).konami(function() {
  return alert('You, my friend, are a geek...');
});
cache = [];
current_tab = null;
plots = {};
data = {};
openTab = function(tab) {
  current_tab = tab;
  if (__indexOf.call(cache, tab) < 0) {
    cache.push(tab);
    switch (tab) {
      case 'phase':
        $('#phaseplot').loading();
        $.getJSON('/data/drphase/', plotPhase);
        break;
      case 'hubble':
        $('[id^="hubbleplot"]').loading();
        $.ajax({
          url: '/data/hubble/',
          dataType: 'json',
          success: plotHubble,
          error: function() {
            $('#tabs').tabs('remove', $('#tabs').tabs('option', 'selected'));
            return alert('No hubblizer info found!');
          }
        });
        break;
      case 'summary':
        $('[id$="_hist"]').loading();
        $('#stack').button().click(function() {
          return toggleStack();
        });
        $.getJSON('/data/drhists/', plotHists);
        break;
      case 'quantity':
        prepareQuantities();
        break;
      case 'spectra':
        prepareSpectra();
        break;
      case 'lc':
        prepareLC();
    }
  }
  if (tab === 'lc' && (globals.openthislc != null)) {
    return plotThisLC();
  }
};
$(function() {
  var t;
  if (window.innerWidth != null) {
    $('[id$="_hist"]').css('width', window.innerWidth / 3.45);
    $('#quantplot').css('width', $('#quantplot').height());
    $('#quanthistx, #quanthisty').css('width', $('#quantplot').height() / 2);
  }
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
  if ($('#tabs').attr('lctarget')) {
    $('#tabs').tabs('select', tabs.indexOf('lc'));
    globals.openthislc = $('#tabs').attr('lctarget');
    $('#tabs').removeAttr('lctarget');
    cache.splice(0, 1);
  }
  openTab(tabs[$('#tabs').tabs('option', 'selected')]);
  $(document).bind('keydown', function(event) {
    return window.currentKey = event.keyCode;
  });
  $(document).bind('keyup', function(event) {
    return window.currentKey = null;
  });
  return true;
});
