'use strict'

var m = require('mithril') // eslint-disable-line no-unused-vars
var Currencies = require('../models/Currencies')
var Tabs = require('./Tabs')
var Utils = require('../utils/Utils')

module.exports = {
  oncreate: Tabs.oncreate,
  onupdate: Tabs.onupdate,
  view: function () {
    return <div class='col m6 s12'>
      <ul class='tabs'>
        {Currencies.map(function (currency) {
          let selectedCurrency = Utils.getRouteParams().currency
          let active
          if (currency === 'total' && selectedCurrency === 'total') {
            active = 'active'
          } else {
            active = currency === selectedCurrency ? 'active' : ''
          }
          return <li class='tab col s1 m2'>
            <a href={'#' + currency} class={active + ' valign-wrapper flex-center'}
              onclick={function () { Utils.setRouteParams(currency, null) }}>
              <span class={currency + '-icon currency-icon'} />
            </a>
          </li>
        })}
      </ul>
    </div>
  }
}
