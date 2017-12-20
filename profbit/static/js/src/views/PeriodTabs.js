'use strict'

var m = require('mithril') // eslint-disable-line no-unused-vars
var Tabs = require('./Tabs')
var PeriodIntervals = require('../models/PeriodIntervals')
var Utils = require('../utils/Utils')

module.exports = {
  oncreate: Tabs.oncreate,
  onupdate: Tabs.onupdate,
  view: function () {
    return <div class='col s12'>
      <ul class='tabs'>
        {Object.keys(PeriodIntervals).map(function (period) {
          let periodName = PeriodIntervals[period]
          let active = period === Utils.getRouteParams().period ? 'active' : ''
          return <li class='tab col s2'>
            <a class={active} href={'#' + period} onclick={function () { Utils.setRouteParams(/* currency= */null, period) }}>
              {periodName}
            </a>
          </li>
        })}
      </ul>
    </div>
  }
}
