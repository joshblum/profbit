'use strict'

var m = require('mithril') // eslint-disable-line no-unused-vars

module.exports = {
  view: function (vnode) {
    return <div class='stats-container container'>
      <div class='tab-row row'>
        {vnode.attrs.tabs}
      </div>
      {vnode.attrs.data}
    </div>
  }
}
