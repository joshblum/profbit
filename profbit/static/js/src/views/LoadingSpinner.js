'use strict'

var m = require("mithril")

module.exports = {
  view: function(vnode) {
    return <div class={"spinner-layer spinner-" + vnode.attrs.color}>
            <div class="circle-clipper left">
              <div class="circle"></div>
            </div><div class="gap-patch">
              <div class="circle"></div>
            </div><div class="circle-clipper right">
              <div class="circle"></div>
            </div>
          </div>
  }
}
