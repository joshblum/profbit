'use strict'

var Tabs = {
  setup: function(vnode) {
    $('ul.tabs').tabs()
  },
}
Tabs.oncreate = Tabs.setup
Tabs.onupdate = Tabs.setup

module.exports = Tabs
