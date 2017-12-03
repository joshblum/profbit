'use strict'
/* global $ */

var Tabs = {
  setup: function (vnode) {
    // Bad hack to get tabs to work.
    $('ul.tabs').tabs()
  }
}
Tabs.oncreate = Tabs.setup
Tabs.onupdate = Tabs.setup

module.exports = Tabs
