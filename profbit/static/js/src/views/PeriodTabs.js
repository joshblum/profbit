'use strict'

var m = require('mithril') // eslint-disable-line no-unused-vars
var Tabs = require('./Tabs')
const periodIntervals = {
  hour: '1h',
  day: '1d',
  week: '1w',
  month: '1m',
  year: '1y',
  all: 'all'
}

module.exports = {
  oncreate: Tabs.oncreate,
  onupdate: Tabs.onupdate,
  view: function () {
    return <div class='col m6 s12'>
      <ul class='tabs'>
        {Object.keys(periodIntervals).map(function (period) {
          let periodName = periodIntervals[period]
          let active = period === m.route.param().period.toLowerCase() ? 'active' : ''
          return <li class='tab col s2'>
            <a class={active} href={'#' + period} onclick={function () {
              m.route.set('/:currency/:period', {
                currency: m.route.param().currency,
                period: period
              })
            }
                       }>
              {periodName}
            </a>
          </li>
        })}
      </ul>
    </div>
  }
}
